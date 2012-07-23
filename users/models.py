from django.db import models
from django.contrib.auth.models import User, Group
from device.models import Device
from application.models import Application

     
"""
Class UserProfile

@date 05/10/2012
@author TKI
"""
class UserProfile(models.Model):
  USERTYPE_CHOICES = (
    (u'A', u'Admin'),
    (u'L', u'Leader'),
    (u'M', u'Member'),
    (u'P', u'Participant'),
  )
  user           = models.ForeignKey(User, unique=True)
#  group          = models.ForeignKey(Group, blank=True, null=True)
#  user = models.OneToOneField(User)
#  devprofile     = models.ForeignKey(DeviceProfile, blank=True, null=True)
#  ub_id          = models.CharField(max_length=30, blank=True, null=True)   
  user_type      = models.CharField(max_length=1, choices=USERTYPE_CHOICES) 
  activation_key = models.CharField(max_length=40)
  key_expires    = models.DateTimeField()


"""
Class UserProfile

@date 07/23/2012
@author TKI
"""
class UserProfile(models.Model):
  USERTYPE_CHOICES = (
    (u'A', u'Admin'),
    (u'L', u'Leader'),
    (u'M', u'Member'),
    (u'P', u'Participant'),
  )
  name           = models.CharField(max_length=50, null=False, unique=True)
  email          = models.CharField(max_length=30, null=False)
  submitted_time = models.DateTimeField()
  approved       = models.BooleanField(default=False)


