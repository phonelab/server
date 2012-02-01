from django.db import models
from django import forms
from application.models import Application

"""
Class DeviceId

@date 01/24/2012
"""
class Device(models.Model):
  id        = models.CharField(max_length=30, null=False, primary_key=True)
  email     = models.CharField(max_length=30, null=False)
  reg_id    = models.CharField(max_length=30, null=False)
  token     = models.CharField(max_length=30, null=True, blank=True)
  created   = models.DateTimeField(auto_now_add=True)
  updated   = models.DateTimeField(auto_now_add=True)


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