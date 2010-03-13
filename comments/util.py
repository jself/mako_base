# PyCrypto and akismet are required;  easy_install them please!
"""Code utilized from http://jmoiron.net"""
from models import *
import akismet
from django.conf import settings

def akismet_check(comment, data={}):
    """Check's a comment with akismet using the API key from settings.  Returns
    a tuple with the akismet class (for further action by the caller) and either
    a True/False value or a literal KeyError class if the key failed validation."""
    req = data
    data = dict(
        user_ip = req.META['REMOTE_ADDR'],
        user_agent = req.META['HTTP_USER_AGENT'],
        referrer = req.META['HTTP_REFERER'],
    )
    ak = akismet.Akismet(settings.AKISMET_KEY, settings.AKISMET_BLOG_URL)
    if ak.verify_key():
        value = ak.comment_check(comment, data=data)
        return ak, value
    else:
        return ak, KeyError

def is_banned(req):
    ip = req.META['REMOTE_ADDR']
    banned =  BannedIp.objects.filter(ip_address = ip)
    return bool(banned)
    
