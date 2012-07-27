from django.db import models
from django.contrib.auth.models import User, Group
from application.models import Application
from device.models import Device

class Experiment(models.Model):
  def irb_count():
    no = Experiment.objects.count()
    if no == None:
      return 1
    else:
      return no + 1
#  group       = models.ForeignKey(Group)
  user        = models.ManyToManyField(User)
  dev         = models.ManyToManyField(Device)
  app         = models.ManyToManyField(Application)
  name        = models.CharField(max_length=50, null=False)
  description = models.CharField(max_length=300, null=False)
  tag         = models.CharField(max_length=10, null=False)
  period      = models.CharField(max_length=5, null=False)
  active      = models.BooleanField(default=False)
  irb         = models.IntegerField(default=irb_count)
  

class ExperimentProfile(models.Model):
  experiment  = models.ForeignKey(Experiment)
  starttime   = models.DateTimeField()
  endtime     = models.DateTimeField()
  link        = models.CharField(max_length=100, blank=True, null=True)





