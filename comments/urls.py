from django.conf.urls.defaults import *


urlpatterns = patterns('finderweb.comments.views',
    # Example:
    # (r'^finderweb/', include('finderweb.foo.urls')),

    # Uncomment this for admin:
   (r'^post/(?P<app>[a-z]+)/(?P<model>[a-z]+)/(?P<id>[0-9]+)/$', 'comments_form'),
   (r'^comments/(?P<app>[a-z]+)/(?P<model>[a-z]+)/(?P<id>[0-9]+)/$', 'render_comments'),



)
