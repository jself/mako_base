from mako import lookup,exceptions
from mako.template import Template
from django.conf import settings
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.template.loaders import app_directories
from johnny.cache import local
import urllib
import copy

def get_page(paginator, request):
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    GET_set("page", page)
    try:
        p = paginator.page(page)
    except (paginator.EmptyPage, paginator.InvalidPage):
        p = paginator.page(paginator.paginator.num_pages)
    return p

def GET_set(var, val):
    local.setdefault("get_args", {})[var] = val

def GET_changed(var, val):
    gets = local.setdefault("get_args", {})
    new_gets = copy.copy(gets)
    new_gets[var] = val
    return urllib.urlencode(new_gets)
    
def GET_all():
    gets = local.setdefault("get_args", {})
    return urllib.urlencode(gets)

def prepare_data(data):
    data['request'] = local.get('request', None)
    data['messages'] = messages
    data['reverse'] = reverse
    data['media_url'] = settings.MEDIA_URL
    for i in (GET_set, GET_changed, GET_all):
        data[i.__name__] = i

TEMPLATE_DIRS = tuple(list(settings.TEMPLATE_DIRS) + list(app_directories.app_template_dirs))
loader = lookup.TemplateLookup(TEMPLATE_DIRS, settings.MODULE_DIR) #, cache_type='memcached', cache_url='localhost')

def render_template(template, **data):
    temp = loader.get_template(template)
    prepare_data(data)
    resp = temp.render_unicode(data=data, **data)
    return resp

def render_string(st, **data):
    prepare_data(data)
    temp = Template(st)
    resp = temp.render_unicode(data=data, **data)
    return resp

def render_to_response(template, **data):
    try:
        prepare_data(data)
        resp = render_template(template, **data)
        return HttpResponse(resp)
    except Exception, e:
        if settings.DEBUG:
            return HttpResponse(exceptions.html_error_template().render())
        else:
            raise e

