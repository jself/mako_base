from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib import admin
from django.contrib.auth.models import User


# Create your models here.
class Ranking(models.Model):
    user = models.ForeignKey(User, null=True)
    ip_address = models.IPAddressField('IP Address', null=True)
    score = models.PositiveSmallIntegerField()
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType)
    related = generic.GenericForeignKey('content_type', 'object_id')
    
admin.site.register(Ranking)
