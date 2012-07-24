from django.db import models
from django import forms
from application.models import Application
from django.contrib.auth.models import User, Group
from django.conf import settings

## other includes
import urllib, urllib2
from urllib2 import URLError
import datetime

"""
Class Device

@date 01/24/2012
"""
class Device(models.Model):
  ACTIVE_CHOICES = (
    (u'E', u'ENABLED'),
    (u'D', u'DISABLED'),
  )
  meid            = models.CharField(max_length=15, null=False)
#  email           = models.CharField(max_length=30, null=False)
  reg_id          = models.CharField(max_length=300, null=False)
  collapse_key    = models.CharField(max_length=255, null=True)
  last_messaged   = models.DateTimeField(blank=True, null=True)
  failed_push     = models.BooleanField(default=False) 
  update_interval = models.CharField(max_length=5, null=False, default=10)
  active          = models.CharField(max_length=1, choices=ACTIVE_CHOICES, null=False)
  created         = models.DateTimeField(auto_now_add=True)
  updated         = models.DateTimeField(auto_now_add=True)

  """
  Send Message to Device

  #curl -X POST https://www.google.com/accounts/ClientLogin -d Email=phone.lab.buffalo@gmail.com -d Passwd=ph0n3l@b -d accountType=HOSTED_OR_GOOGLE -d service=ac2dm

  @date 02/06/2012
  @param Boolean delay_while_idle

  @author Micheal
  """
  def send_message(self, delay_while_idle = False, **kwargs):
    C2DM_URL = "https://android.apis.google.com/c2dm/send"
    if self.failed_push:
      return

    values = {
      'registration_id': self.reg_id,
      'collapse_key': 0,
    }

    if delay_while_idle:
      values['delay_while_idle'] = ''

    for key,value in kwargs.items():
      values['data.%s' % key] = value

    headers = {
      'Authorization': 'GoogleLogin auth=%s' % settings.C2DM_AUTH_TOKEN,
    }

    try:
      params = urllib.urlencode(values)
      request = urllib2.Request(C2DM_URL, params, headers)
      # make request
      response = urllib2.urlopen(request)
      # get result
      result = response.read().split('=')
      if 'Error' in result:
        if result[1] == 'InvalidRegistration' or result[1] == 'NotRegistered':
          self.failed_push = True
          self.save()
        raise Exception(result[1])
      return result
    except URLError:
      return False
    except Exception, error:
      return False 

  def __unicode__(self):
    return '%s' % self.id

"""
Send Message to multiple devices

@date 02/06/2012
@param Array device_list
@author Micheal
"""

def send_multiple_messages(device_list, **kwargs):
	for device in device_list:
		device.send_message(kwargs)

"""
Class DeviceApplication

@date 01/24/2012
"""
class DeviceApplication(models.Model):
  dev    = models.ForeignKey(Device)
  app    = models.ForeignKey(Application)
#  action    = models.CharField(max_length=30, null=False)
  class Meta:
#    unique_together= (('app', 'action'),)
    unique_together= (('dev', 'app'),)

"""
Class DeviceProfile

@data 05/10/2012
@author TKI
"""
class DeviceProfile(models.Model):
  STATUS_CHOICES = (
    (u'L', u'Lost'),
    (u'N', u'Not Working'),
    (u'O', u'Out of Order'),
    (u'W', u'Working'),
  )
  PURPOSE_CHOICES = (
    (u'C1', u'CSE622'),
    (u'C2', u'CSE646'),
    (u'C3', u'CSExxx'),
    (u'F', u'Faculty Use'),
    (u'O', u'Other'),
    (u'P', u'PhoneLab'),
    (u'R', u'Research'),
    (u'N', u'Not Assigned'),
  )
  TYPE_CHOICES = (
    (u'3', u'3G'),
    (u'4', u'4G'),
  )
  dev                = models.ForeignKey(Device, unique=True)
  user               = models.ForeignKey(User, blank=True, null=True)
#  group              = models.ManyToManyField(Group, blank=True, null=True)
  last_log           = models.DateTimeField(blank=True, null=True)
  phone_no           = models.CharField(max_length=13, blank=True, null=True)
  status             = models.CharField(max_length=1, choices=STATUS_CHOICES)
  plan               = models.CharField(max_length=45, blank=True, null=True)
  image_version      = models.CharField(max_length=45, blank=True, null=True)
  purpose            = models.CharField(max_length=2, choices=PURPOSE_CHOICES)
  service_type       = models.CharField(max_length=1, choices=TYPE_CHOICES)
  install_permission = models.BooleanField(default=False)
