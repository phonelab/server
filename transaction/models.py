from django.db import models
from application.models import Application
from device.models import Device

"""
Class Transaction

@date 04/06/2012
"""
class Transaction(models.Model):
  STATUS_CHOICES = (
    (u'S', u'Start'),
    (u'P', u'Progress'),
    (u'C', u'Complete'),
  )
  user               = models.ForeignKey(User)
  # status: start, progress and complete
  status             = models.CharField(max_length=1, choices=STATUS_CHOICES, null=False)
  start              = models.DataTimeField(auto_now_add=True)
  end                = models.DataTimeField()
# last_manifest_send = models.DataTimeField()


"""
Class Transaction

@date 04/06/2012
"""
class Transaction(models.Model):
#Do To: change name
  STATUS_CHOICES = (
    (u'Y', u'Install'),
    (u'N', u'Uninstall'),
  )
  device = models.ForeignKey(Device)
  app    = models.ForeignKey(Application)
  # status: Y or N, defalut is N, which means uninstall
  status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="N", null=False)
#  class Meta:
#    unique_together= (('device', 'app'),)

