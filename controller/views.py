from django.http import HttpResponse
from controller.models import Application, Device, DeviceApplication
from django.shortcuts import render

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
def download_manifest(request, deviceId): 
  device = Device.objects.filter(id=deviceId)
  # device exists
  if device.count() == 1:
    device = device[0]
    app_list = {}
    apps = {}
    # get apps of particular device
    for o in DeviceApplication.objects.filter(device=device.id).values('app', 'action'):
      app_list[o['app']] = o['action']
    # get list of apps to download
    for app in Application.objects.filter(id__in=app_list.keys()):
      apps[app.id] = {"app_object": app, "app_status": app_list[app.id]}
    # apps present
    if len(apps) > 0 :
      print apps
      return render(request,
        'manifest/success.xml', 
        {
            'deviceId':deviceId
          , 'apps': apps
        },
        content_type="application/xml"
      )
    # no apps present
    else :
      return render(request,
      'manifest/fail.xml', 
      {
          msg: "apps not found"
      },
      content_type="application/xml"
    )
  # device does not exist
  else :
    return render(request,
      'manifest/fail.xml', 
      {
          msg: "deviceID not found"
      },
      content_type="application/xml"
    )