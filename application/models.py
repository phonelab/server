from django.db import models
from django import forms
from django.contrib.auth.models import User, Group

"""
Class Application

@date 01/24/2012
"""
class Application(models.Model):
  ACTIVE_CHOICES = (
    (u'E', u'ENABLED'),
    (u'D', u'DISABLED'),
  )
  TYPE_CHOICES = (
    (u'B', u'BACKGROUND'),
    (u'I', u'INTERACTIVE'),
  )
  name          = models.CharField(max_length=30, null=False)
  user          = models.ForeignKey(User, null=False)
#  group         = models.ForeignKey(Group, blank=True, null=True)
  package_name  = models.CharField(max_length=100, null=False)
#  intent_name   = models.CharField(max_length=100, null=False)
  description   = models.CharField(max_length=255, null=True, blank=True)
  type          = models.CharField(max_length=1, choices=TYPE_CHOICES)
  starttime     = models.DateTimeField(null=True, blank=True)
  endtime       = models.DateTimeField(null=True, blank=True)
#  version       = models.CharField(max_length=10, null=False)
  active        = models.CharField(max_length=1, choices=ACTIVE_CHOICES, null=False)
  created       = models.DateTimeField(auto_now_add=True)
  updated       = models.DateTimeField(auto_now_add=True)
  def __unicode__(self):
    return self.name
