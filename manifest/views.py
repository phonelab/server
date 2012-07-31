from django.http import HttpResponse
from application.models import Application
from device.models import Device, DeviceApplication, DeviceProfile
from transaction.models import TransactionDevApp
from experiment.models import Experiment
from django.shortcuts import render
from lib.helper import json_response_from, json
from django.contrib.auth.models import User, Group

"""
Generate Manifest based on deviceId

@date 01/24/2012
@param String deviceId

@author Micheal

# <b>Stub to create New Devices</b>
#
# from controller.models import Application, Device, DeviceApplication
# import datetime
# d = Device(id='123', email='micheala@buffalo.edu')
# d.save()
# a = Application(name='TestCat', package_name='com.phonelab.testcat', intent_name='Main.intent', description='asdasd', type='sync', starttime=datetime.datetime.now(), endtime=datetime.datetime.now(), download='/application/testcat.apk', version='1.0')
# b = Application(name='Calender', package_name='com.google.calender', intent_name='Main.intent', description='awesome google clender', type='async', starttime=datetime.datetime.now(), endtime=datetime.datetime.now(), download='/application/calender.apk', version='1.5.1')
# a.save()
# b.save()
#
"""
def download_manifest(request, deviceId): 
  # define default response
  response = { "error": "", "data": "" }
  try:
    #if device exists
    print deviceId
    dev = Device.objects.get(meid=deviceId) 
    app_list = {}
    apps = {}
    tags = {}
    # get apps of particular device
    print dev
    for o in TransactionDevApp.objects.filter(dev=dev).filter(result="N").values('app', 'action'):
    # get list of apps to download
      for app in Application.objects.filter(id=o['app']):
        if o['action'] == "I":
          apps[app.id] = {"app_object": app, "app_status": "install"}
        else:  
          apps[app.id] = {"app_object": app, "app_status": "uninstall"}
      print "Here" 
    #get tag names from experiments
      for dev in Experiment.dev.all():
        print dev.meid
#    deviceprofile = Experiment.objects.get(dev=dev)
#    for device in deviceprofile.group.all():
#      for experiment in Experiment.objects.filter(=group.id):
#        tags[group.id] = experiment.tag
      
    return render(
      request,
      'manifest/success.xml', 
      {
          'deviceId'                    : deviceId, 
          'status_monitor_update_value' : dev.update_interval, 
          'apps'                        : apps,
          'tags'                        : tags
      },
      content_type="application/xml"
    )
  # device does not exist
  except Device.DoesNotExist :
    return render(
      request,
        'manifest/fail.xml', 
        {
            'no' : 'err1'
          , 'msg': 'invalid device'
        },
        content_type="application/xml"
      )
  return json_response_from(response)
