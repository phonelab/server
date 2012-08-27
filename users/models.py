from django.db import models
from django.contrib.auth.models import User, Group
from device.models import Device
from application.models import Application
from datetime import datetime


     
"""
Class UserProfile

@date 05/10/2012
@author TKI
"""
class UserProfile(models.Model):
  USERTYPE_CHOICES = (
    (u'A', u'Admin'),
    (u'E', u'Experimenter'),
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
Class Participant

@date 07/23/2012
@author TKI
"""
class Participant(models.Model):
  STUDENT_CHOICES = (
    (u'F', 'Freshman'),
    (u'SO', 'Sophomore'),
    (u'J', 'Junior'),
    (u'SE', 'Senior'),
    (u'G', 'Graduate'),
    (u'P','PhD'),
    )
  name           = models.CharField(max_length=50, null=False)
  email          = models.CharField(max_length=30, null=False)
  submitted_time = models.DateTimeField()
  approved       = models.BooleanField(default=False)
  student_status = models.CharField(max_length=2, choices=STUDENT_CHOICES)
  expected_grad = models.DateField(blank=True, null=True)
  # def batch(self):


  

class ParticipantRegister(models.Model):
  lib_number     = models.CharField(max_length=14, null=False)
  meid           = models.CharField(max_length=15, null=False)
  approved       = models.BooleanField(default=False)
  
