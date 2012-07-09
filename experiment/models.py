from django.db import models
from django.contrib.auth.models import User, Group
from application.models import Application
from device.models import Device
from transaction.models import Transaction

class ExperimentProfile(models.Model):
  members     = models.ForeignKey(Group)
  dev         = models.ManyToManyField(Device)
  app         = models.ManyToManyField(Application)
  tid         = models.ManyToManyField(Transaction)
  name        = models.CharField(max_length=50, null=False)
  description = models.CharField(max_length=300, null=False)
  tag         = models.CharField(max_length=10, null=False)


class LeaderExperimentProfile(models.Model):
  leader      = models.ForeignKey(User)
  experiment  = models.ForeignKey(ExperimentProfile)
  class Meta:
    unique_together= (('leader', 'experiment'),)
