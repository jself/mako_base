from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib import admin
import threading


# Create your models here.
class Comment(models.Model):
    user = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    email = models.EmailField()
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType)
    related = generic.GenericForeignKey('content_type', 'object_id')
    in_moderation = models.BooleanField(blank=True)
    ip_address = models.IPAddressField('IP Address', null=True)
    
    def __unicode__(self):
        return "%s - %s (%s)" % (self.user, self.title, self.created.strftime('%m/%d/%Y'))

    class Meta:
        ordering = ('-created',)

    def save(self, *args, **kwargs):
        threading.Thread(None, x).start()
        return super(Comment, self).save(*args, **kwargs)


class BannedIp(models.Model):
    timestamp = models.DateTimeField('Date/Time banned', auto_now_add=True)
    ip_address = models.IPAddressField('IP Address')

admin.site.register(Comment)
admin.site.register(BannedIp)
