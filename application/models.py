from django.db import models
from django import forms

"""
Class Application

@date 01/24/2012
"""
class Application(models.Model):
  ACTIVE_CHOICES = (
    (u'E', u'ENABLED'),
    (u'D', u'DISABLED'),
  )
  name          = models.CharField(max_length=30, null=False)
  package_name  = models.CharField(max_length=100, null=False)
  intent_name   = models.CharField(max_length=100, null=False)
  description   = models.CharField(max_length=255, null=True, blank=True)
  type          = models.CharField(max_length=30)
  starttime     = models.DateTimeField(null=True, blank=True)
  endtime       = models.DateTimeField(null=True, blank=True)
  version       = models.CharField(max_length=10, null=False)
  active          = models.CharField(max_length=1, choices=ACTIVE_CHOICES, null=False)
  created       = models.DateTimeField(auto_now_add=True)
  updated       = models.DateTimeField(auto_now_add=True)
  def __unicode__(self):
    return self.name
