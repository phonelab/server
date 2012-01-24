from django.db import models
from django import forms

"""
Class DeviceId

@date 01/24/2012
"""
class Device(models.Model):
  id        = models.CharField(max_length=30, null=False, primary_key=True)
  email     = models.CharField(max_length=30, null=False)
  created   = models.DateTimeField(auto_now_add=True)
  updated   = models.DateTimeField(auto_now_add=True)

"""
Class Application

@date 01/24/2012
"""
class Application(models.Model):
  name          = models.CharField(max_length=30, null=False)
  package_name  = models.CharField(max_length=100, null=False)
  intent_name   = models.CharField(max_length=100, null=False)
  description   = models.CharField(max_length=255, null=True, blank=True)
  type          = models.CharField(max_length=30)
  starttime     = models.DateTimeField(null=True, blank=True)
  endtime       = models.DateTimeField(null=True, blank=True)
  download      = models.CharField(max_length=255, null=False)
  version       = models.CharField(max_length=10, null=False)
  created       = models.DateTimeField(auto_now_add=True)
  updated       = models.DateTimeField(auto_now_add=True)

"""
Class DeviceApplication

@date 01/24/2012
"""
class DeviceApplication(models.Model):
  device    = models.ForeignKey(Device)
  app       = models.ForeignKey(Application)
  action    = models.CharField(max_length=30, null=False)
  class Meta:
    unique_together= (('app', 'action'),)