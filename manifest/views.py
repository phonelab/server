from django.http import HttpResponse
from application.models import Application
from device.models import Device, DeviceApplication
from transaction.models import TransactionDevApp
from django.shortcuts import render
from lib.helper import json_response_from, json

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
# a = Application(name='TestCat', package_name='com.phonelab.testcat', intent_name='Main.intent', description='asdasd', type='sync', starttime=datetime.datetime.now(), endtime=datetime.datetime.now(), download='/experiment/testcat.apk', version='1.0')
# b = Application(name='Calender', package_name='com.google.calender', intent_name='Main.intent', description='awesome google clender', type='async', starttime=datetime.datetime.now(), endtime=datetime.datetime.now(), download='/experiment/calender.apk', version='1.5.1')
# a.save()
# b.save()
#
"""
def download_manifest(request, deviceId): 
  # define default response
  response = { "error": "", "data": "" }
  try:
    #if device exists
    dev = Device.objects.get(id=deviceId) 
    app_list = {}
    apps = {}
    # get apps of particular device
    for o in TransactionDevApp.objects.filter(dev=dev.id).filter(result="N").values('app', 'action'):
    # get list of apps to download
      for app in Application.objects.filter(id=o['app']):
        if o['action'] == "I":
          apps[app.id] = {"app_object": app, "app_status": "install"}
        else:  
          apps[app.id] = {"app_object": app, "app_status": "uninstall"}
    return render(
      request,
      'manifest/success.xml', 
      {
          'deviceId'                    : deviceId
        , 'status_monitor_update_value' : dev.update_interval
        , 'apps'                        : apps
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
