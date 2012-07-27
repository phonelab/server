from django.db import models
from django.contrib.auth.models import User
from application.models import Application
from device.models import Device
from experiment.models import Experiment

"""
Class Transaction

@date 04/06/2012
"""
class Transaction(models.Model):
#  STATUS_CHOICES = (
#    (u'P', u'Progress'),
#    (u'C', u'Complete'),
#  )
  user               = models.ForeignKey(User)
  eid                = models.ForeignKey(Experiment)
  total              = models.IntegerField(null=False) 
  progress           = models.IntegerField(null=False)
  # status: start, progress and complete
#  status             = models.CharField(max_length=1, choices=STATUS_CHOICES, null=False)
  start              = models.DateTimeField(auto_now_add=True)
  end                = models.DateTimeField(blank=True, null=True)
  processed          = models.BooleanField(default=False)
# last_manifest_send = models.DateTimeField()
  def __unicode__(self):
    return str(self.id)

"""
Class Transaction

@date 04/06/2012
"""
class TransactionDevApp(models.Model):
#Do To: change name
  ACTION_CHOICES = (
    (u'I', u'Install'),
    (u'U', u'Uninstall'),
  )
  RESULT_CHOICES = (
    (u'N', u'N/A'),
    (u'S', u'Success'),
    (u'F', u'Failure'),
    (u'F1', u'FailureAlreadyInstalled'),
    (u'F2', u'FailureNoSuchApplication'),
  )
  tid      = models.ForeignKey(Transaction)
  dev      = models.ForeignKey(Device)
  app      = models.ForeignKey(Application)
  # action: I or U, I means uninstall, U means uninstall
  action   = models.CharField(max_length=1, choices=ACTION_CHOICES, null=False)
  result   = models.CharField(max_length=2, choices=RESULT_CHOICES, default="N" , null=False)
  start    = models.DateTimeField(auto_now_add=True)
  end      = models.DateTimeField(blank=True, null=True)
  class Meta:
    unique_together= (('tid', 'dev', 'app'),)
