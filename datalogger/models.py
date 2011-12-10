from django.db import models
from django import forms

class LogFile(models.Model):
  deviceId = models.CharField(max_length=30, null=False)
  logFile = models.CharField(max_length=30, null=False)
  updated = models.DateTimeField(auto_now_add=True)
  def __unicode__(self):
    return self.deviceId