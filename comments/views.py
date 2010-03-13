# Create your views here.
from django.contrib.contenttypes.models import ContentType
from models import Comment
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django import forms
from utils import *
import simplejson
from django.contrib import messages
from util import *

class CommentForm(forms.Form):
    user = forms.CharField(label="Name", max_length=255)
    email = forms.EmailField(max_length=255)
    title = forms.CharField(max_length=255)
    text = forms.CharField(max_length=5000, widget=forms.Textarea)

def comments_for_item(app, model, id, page=None):
    page = page if page else 1
    GET_set("comment_page", page)
    try:
        content_type = ContentType.objects.get(app_label=app, model__iexact=model)
    except ContentType.DoesNotExist:
        raise Http404

    comments = Comment.objects.filter(content_type=content_type, object_id=id, in_moderation=False).order_by('-created')

    paginator = Paginator(comments, 5)
    try:
        comments = paginator.page(page)
    except (EmptyPage, InvalidPage):
        comments = paginator.page(paginator.num_pages)
    return comments

def render_comments(request, app, model, id, form=None, direct=False):
    page = request.GET.get('comment_page', 1)
    GET_set("comment_page", page)
    comments = comments_for_item(app, model, id, page)
    if direct:
        return render_template('widgets/comments/comments.html', comments=comments, form=form, app=app, model=model, id=id)
    return render_to_response('widgets/comments/comments.html', comments=comments, form=form, app=app, model=model, id=id)

def comments_form(request, app, model, id, direct=False):
    if request.method == 'GET':
        form = CommentForm()
    else:
        form = CommentForm(request.POST)
        save = True
        if form.is_valid():
            if is_banned(request):
                save = False
                return HttpResponse('Your IP address has been banned. Please contact the \
                               administrator if you believe this to be in error.')
            else:
                try:
                    content_type = ContentType.objects.get(app_label=app, model__iexact=model)
                    model = content_type.model_class()
                    instance = model.objects.get(pk=id)
                except:
                    messages.error(request, 'Error posting form.')
                    raise Http404
            
            akismet, is_spam = akismet_check(form.cleaned_data['text'], request)
            ip = request.META['REMOTE_ADDR']
            form.cleaned_data['ip_address'] = ip
            if is_spam:
                form.cleaned_data['in_moderation'] = True
                response = "Your submission has been marked for manual moderation due to the possibility of spam. It will be checked shortly."
            else:
                form.cleaned_data['in_moderation'] = False
                response = "Success"
            form.cleaned_data['related'] = instance
            comment = Comment(**form.cleaned_data)
            comment.save()
            return HttpResponse(response)
    if direct:
        return render_template('widgets/comments/form.html', app=app, model=model, id=id, form=form)
    return render_to_response('widgets/comments/form.html', app=app, model=model, id=id, form=form)
