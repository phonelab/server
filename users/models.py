from django.db import models
from django.contrib.auth.models import User
from device.models import Device

     
"""
Class UserProfile

@date 05/10/2012
@author TKI
"""
class UserProfile(models.Model):
  user           = models.ForeignKey(User, unique=True)
#  user = models.OneToOneField(User)
  dev            = models.ForeignKey(Device, blank=True, null=True)
  name           = models.CharField(max_length=45, blank=True, null=True)    
  ub_id          = models.CharField(max_length=30, blank=True, null=True)   
  activation_key = models.CharField(max_length=40)
  key_expires    = models.DateTimeField()
