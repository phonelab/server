from django.db import models
from django import forms
from application.models import Application
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
  id              = models.CharField(max_length=30, null=False, primary_key=True)
  email           = models.CharField(max_length=30, null=False)
  reg_id          = models.CharField(max_length=30, null=False)
  collapse_key    = models.CharField(max_length = 50)
  last_messaged   = models.DateTimeField(blank = True, default = datetime.datetime.now)
  failed_push     = models.BooleanField(default = False)
  update_interval = models.CharField(max_length=5, null=False, default=10)
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
      'registration_id': self.registration_id,
      'collapse_key': self.collapse_key,
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
    except URLError:
      return false
    except Exception, error:
      return false 

  """
  Send Message to multiple devices

  @date 02/06/2012
  @param Array device_list

  @author Micheal
  """
  def send_multiple_messages(device_list, **kwargs):
    for device in device_list:
      device.send_message(kwargs)

  def __unicode__(self):
    return '%s' % self.id

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