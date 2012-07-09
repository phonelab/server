from django.db import models
from django.contrib.auth.models import User
#from device.models import DeviceProfile

     
"""
Class UserProfile

@date 05/10/2012
@author TKI
"""
class UserProfile(models.Model):
  user           = models.ForeignKey(User, unique=True)
  ub_id          = models.CharField(max_length=30, blank=True, null=True)   
  activation_key = models.CharField(max_length=40)
  key_expires    = models.DateTimeField()
  user_type 	 = models.CharField(max_length=20)
