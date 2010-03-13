from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    (r'^login/$', views.login),
    (r'^logout/$', views.logout),
    (r'^register/$', views.register),
    (r'^forgot_pass/$', views.forgot_pass),
)

