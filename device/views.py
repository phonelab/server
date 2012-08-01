from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import RequestContext

#from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from lib.helper import json_response_from, json
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from users.forms import ParticipantForm

#from manifest.views import *
from device.models import Device, DeviceApplication, DeviceProfile
from device.models import HeartbeatStatus, OtaStatus
from users.models import UserProfile
from application.models import Application
from transaction.models import Transaction, TransactionDevApp
from utils import re_sort_nicely, sort_nicely, is_valid_device
#from users.views import is_member, is_leader
import os, errno, re
import string

# Log Dir
RAW_LOG_ROOT = settings.RAW_LOG_ROOT

"""
Main page

@date 03/05/2012

@author Taeyeon
"""
def main_page(request):
  return render_to_response(
           'index.html',
           { 
           'user': request.user },
           context_instance=RequestContext(request)
         )

"""
List All Devices

@date 02/07/2012

@author Micheal
"""
"""
Update to show only the user's device

@date 07/09/2012

@author Manoj
"""
@login_required
#@login_required(login_url='/login/')
def index(request):
  user = request.user
  userprofile = UserProfile.objects.get(user = user)
  group = []
  #initialize devices
  devices = {}
  if userprofile.user_type == 'P':
    # get user's devices
    device_profiles = DeviceProfile.objects.filter(user=user)

  if userprofile.user_type == 'A':
    device_profiles = DeviceProfile.objects.all()

  if userprofile.user_type == 'E':
    device_profiles = DeviceProfile.objects.filter(group = userprofile.group)
    
  for device in device_profiles:
    devices[device] = Device.objects.filter(id = device.dev.id).order_by('-created')
  
  return render_to_response(
            'device/index.html', 
            {    
                'userprofile': userprofile,
                'devices': devices
            },   
            context_instance=RequestContext(request)
          )

"""

@date 01/29/2012

@param id IMEI number
@param email email
@param reg_id Registration Id

# Create new device
# curl -X POST -d "device_id=123&email=micheala@buffalo.edu&reg_id=some_id" http://107.20.190.88/device/

@api public

@author Micheal
"""
def create_or_update_device(request): 
  # define default response
  response = { "error": "", "data": "" }
  # return if GET request
  if request.method == 'GET':
    response['error'] = {
      'no' : 'err0',
      'msg': 'sorry no gets'
    }
    return json_response_from(response)
  # get params from POST
  params = request.POST
  # error checking
  if (params['device_id'] == "" or params['reg_id'] == ""):
    response['error'] = {
      'no' : 'err1',
      'msg': 'missing mandatory params'
    }
  # get device
  device = Device.objects.filter(meid=params['device_id'])
  # if device exists, update
  if device.count() == 1:
    device = device[0]
    # email
    #if ('email' in params and device.email != params['email']):
    #  device.email = params['email']
    # reg_id
    if ('reg_id' in params and device.reg_id != params['reg_id']):
      device.reg_id = params['reg_id']
    # update
    if ('update_interval' in params and device.update_interval != params['update_interval']):
      device.update_interval = params['update_interval']
  # device does not exist, insert
  else:
    device = Device(
        meid     = params['device_id'], 
    #    email  = "phonelab@gmail.com", #params['email'] 
        reg_id = params['reg_id']
    )
  # save device
  device.save()
  
  # device
  response['data'] = device
  # render json response
  return json_response_from(response)


"""
Show Device Details and Application monitor [GET]

@date 05/17/2012
@param String deviceId

@author TKI, Micheal
"""
@login_required
def show(request, deviceId):
  user = request.user
  userprofile = UserProfile.objects.get(user_id=user.id)
  # define default response
  response = { "err": "", "data": "" }

  #check deviceId to control accesses
  if is_valid_device(user, deviceId):
    # get device
    try:
      dev = Device.objects.get(id=deviceId)
      # device exists
      app_list = {}
      apps = {}
      unapps = {}
      # get apps of particular device
      for o in DeviceApplication.objects.filter(dev=dev.id).values('app', 'dev'):
        app_list[o['app']] = o['dev']
      # get list of apps to download
      for app in Application.objects.all():
        if app_list.has_key(app.id):
          apps[app.id] = {"app_object": app,}
        else:
          unapps[app.id] = {"app_object": app,}

      # get log data list from deviceId directory
      path = os.path.join(RAW_LOG_ROOT, dev.meid)
      # empty
      filelist = {}
      try:
        os.chdir(path)
        filelist = os.listdir(".")
        re_sort_nicely(filelist)

      except OSError, e:
        if e.errno != errno.EEXIST:
          response['err'] = {
            'no' : 'err1', 
            'msg': 'cannot change dir, failed upload'
          }
      return render_to_response(
    	  'device/show.html', 
  	    {
    	    'device' : dev,
    	    'apps'     : apps,
          'unapps'   : unapps,
          'filelist' : filelist,
          'userprofile': userprofile,
#          'group': userprofile.group
    	  },
        context_instance=RequestContext(request)
      )
    
    # device does not exist
    except Device.DoesNotExist: 
      response['err'] = {
        'no' : 'err1',
        'msg': 'invalid device'
      }
    return json_response_from(response)
  else:
    return HttpResponseRedirect('/')

"""
Edit Device Form [GET]

@date 02/08/2012
@param String deviceId

@author Micheal
"""
@login_required
def edit(request, deviceId):
  user = request.user
  # define default response
  response = { "err": "", "data": "" }

  #check deviceId to control accesses
  if is_valid_device(user, deviceId):
    # get device
    try:
      device = Device.objects.get(id=deviceId)
      # device exists
      return render_to_response(
        'device/edit.html', 
          {
            'device': device
          },
          context_instance=RequestContext(request)
        )
    # device does not exist
    except Device.DoesNotExist: 
      response['err'] = {
        'no' : 'err1',
        'msg': 'invalid device'
      }
    return json_response_from(response)
  else:
    return HttpResponseRedirect('/')

"""
Update Device Via Form [POST]

@date 02/08/2012
@param String deviceId

@author Micheal
"""
def update(request, deviceId):
  # define default response
  response = { "err": "", "data": "" }
  # return if GET request
  if request.method == 'GET':
    response['err'] = {
      'no' : 'err0',
      'msg': 'sorry no gets'
    }
    return HttpResponseRedirect('/error/')
  # get params from POST
  params = request.POST
  # get device
  device = Device.objects.filter(id=deviceId)
  # if device exists, update
  if device.count() == 1:
    #
    device = device[0]
    # email
    #if ('email' in params and device.email != params['email']):
    #  device.email = params['email']
    # reg_id
    if ('reg_id' in params and device.reg_id != params['reg_id']):
      device.reg_id = params['reg_id']
    # update
    if ('update_interval' in params and device.update_interval != params['update_interval']):
      device.update_interval = params['update_interval']
    # save device
    device.save()
    # redirect to device/<deviceId>
    return HttpResponseRedirect('/device/' + str(device.id))
  # device does not exist
  else:
    return HttpResponseRedirect('/error/')


"""
Send message to a phone using C2DM [POST]

@date 02/09/2012
@param String deviceId
@c2dm_mag message string

@author Taeyeon
"""
def c2dm(request, deviceId):
  # define default response
  response = { "err": "", "data": "" }
  # return if GET request
  if request.method == 'GET':
    response['err'] = {
      'no' : 'err0',
      'msg': 'sorry no gets'
    }
  else:	
    msg = request.POST['c2dm_msg']
    # get device
    try:
      dev = Device.objects.get(id=deviceId)
      # msg = "new_manifest"
      #TODO: Implement other messages.
      response = dev.send_message(payload=json({"message": msg}))
    except Device.DoesNotExist: 
      response['err'] = {
        'no' : 'err1',
        'msg': 'invalid device'
      }
    return json_response_from(response)		

"""
Status monitor [GET]

@date 02/20/2012
@param String deviceId
@param String statusType

@author Taeyeon
"""
@login_required
def status(request, deviceId, statusType):
  user = request.user
  # define default response
  response = { "err": "", "data": "" }

  #check deviceId to control accesses
  if is_valid_device(user, deviceId):
    # get device
    try:
      device = Device.objects.get(id=deviceId)
      # device exists
      # get log data list from deviceId directory
      path = os.path.join(RAW_LOG_ROOT, device.meid)
      # empty
      filelist = {}
      tagName = ''
      if statusType == '1':
        tagName = 'Battery_level'
        #tagName = 'Battery level'
      elif statusType == '2':
        tagName = 'Location_Latitude'
        #tagName = 'Location: Latitude'
      else:
        tagName = 'Signal_Strength'
        #tagName = 'Signal Strength'
      try:
        os.chdir(path)
        filelist = os.listdir(".")
        sort_nicely(filelist)
        Tagdata = ''
        for file in filelist:
          filename = os.path.join(RAW_LOG_ROOT, device.meid, file)
          Logfile = open(filename, 'r+')
          for line in Logfile:
            #Logdata = Logfile.readline()
            if re.search(tagName, line):
              temp = line.split()
              Tagdata += ' [ ' + temp[0] + ' ' + temp[1] + ' ] '
              if statusType == '1':
                Tagdata += 'Battery Level: ' + temp[7] + '\n'
              elif statusType == '2':
                Tagdata += 'GPS Latitude: ' + temp[7] + ', Longitude: ' + temp[9] + ', Accuracy: ' + temp[11] + '\n'
              else:
                Tagdata += 'Signal Strengh: ' + temp[7] + ', asu: ' + temp[9] + '\n'

        # render respone
        return render_to_response(
          'device/status.html',
          {
            'device': device,
            'TagName': tagName,
            'Tagdata': Tagdata
          },
          context_instance=RequestContext(request)
        )
        Logfile.close()
        Tagfile.close()
      except OSError, e:
        if e.errno != errno.EEXIST:
          response['err'] = {
            'no' : 'err1', 
            'msg': 'cannot change dir'
          }
    # device does not exist
    except Device.DoesNotExist: 
      response['err'] = {
        'no' : 'err1',
        'msg': 'invalid device'
      }
    return json_response_from(response)
  else:
    return HttpResponseRedirect('/')


"""
Insert DeviceApplication DB [POST]
Update DeviceApplication DB [POST]
Delete DeviceApplication DB [POST]
@date 03/30/2012

@param dev_id
@param app_id
@param action (I: install, U: uninstall)
@param result (S: success, F: failure)

# Insert DeviceApplication DB using POST method
# curl -X POST -d "dev_id=A000002A000000&app_id=2&app_id=3&action=I&result=S" http://107.20.190.88/deviceapplication/
# curl -X POST -d "dev_id=A000002A000000&app_id=1&app_id=2&action=I&action=U&result=S&result=F" http://localhost:8000/deviceapplication/

@author TKI
"""
def insert_or_update_deviceapplication(request): 
  # define default response
  response = { "error": "", "data": "" }
  # return if GET request
  if request.method == 'GET':
    response['error'] = {
      'no' : 'err0',
      'msg': 'sorry no gets'
    }
    return json_response_from(response)
  # params checking
  if not (request.POST.has_key('dev_id') and request.POST.has_key('app_id') \
          and request.POST.has_key('action') and request.POST.has_key('result')):
    response['error'] = {
      'no' : 'err1',
      'msg': 'missing mandatory params'
    }
    return json_response_from(response)

  app_ids = request.POST.getlist('app_id')
  actions = request.POST.getlist('action')
  results = request.POST.getlist('result')
  num = 0
  # data check
  try:
    dev = Device.objects.get(meid=request.POST['dev_id'])
    for app_id in app_ids:
      try:
        app = Application.objects.get(id=app_id)
        #if result is Success
        if results[num] == "S":
          #if action is install
          if actions[num] == "I":
            devapp = DeviceApplication()
            if DeviceApplication.objects.filter(dev=dev).filter(app=app):
              response['err'] = {
                'no' : 'err1',
                'msg': 'has the information already'
              }
              return json_response_from(response)
            devapp.app = app  
            devapp.dev = dev
            devapp.save()
          else: 
          #if action is uninstall
            try:
              devapp = DeviceApplication.objects.filter(dev=dev).filter(app=app)
              devapp.delete()
            # deviceapplication does not exist
            except DeviceApplication.DoesNotExist:
              response['err'] = {
                'no' : 'err1',
                'msg': 'invalid deviceapplication'
              }
              return json_response_from(response)
           
        #update the result in TransactionDevApp table
        #update the status in Transaction
        #TODO: improve this logic
        try:
#          for i in TransactionDevApp.objects.filter(dev=dev).filter(app=app).filter(action=actions[num]).filter(result="N"):
          for i in TransactionDevApp.objects.filter(dev=dev).filter(app=app).filter(result="N"):
            count = TransactionDevApp.objects.filter(id=i.id).update(result=results[num], end=datetime.now())
            trans = Transaction.objects.get(id=i.tid.id)
            if trans.total ==  trans.progress + count:
              trans.end = datetime.now()
            trans.progress += count     #progress/ total
            trans.save()
            if not TransactionDevApp.objects.filter(dev=dev).filter(result="N"):
              Device.objects.filter(id=dev).update(active="E")
#            Application.objects.filter(id=app).update(active="E")
        # TransactionDevApp does not exist
        except TransactionDevApp.DoesNotExist:
          response['err'] = {
            'no' : 'err1',
            'msg': 'invalid TransactionDevApp'
          }
          return json_response_from(response) 
        num = num + 1
      # application does not exist
      except Application.DoesNotExist:
        response['err'] = {
          'no' : 'err1',
          'msg': 'invalid application'
        }
        return json_response_from(response)
  # device does not exist
  except Device.DoesNotExist:
    response['err'] = {
      'no' : 'err1',
      'msg': 'invalid device'
      }
    return json_response_from(response)
  
  return json_response_from(response)

"""
Update DeviceStatus DB [POST]
@date 07/26/2012

@param device_id
@param status_type (H: heart beat, O: OTA feedback, Ob: new build version 2: reserved)
@param status_value (H => 0: no problem , 1: There is some wrong)
@param status_value (O => 1: download completed, 2)
@param status_value (Ob => new build version, string type)

# Insert DeviceApplication DB using POST method
# curl -X POST -d "device_id=A000002A000000&status_type=H&status_value=0" http://107.20.190.88/devicestatus/
# curl -X POST -d "device_id=A000002A000000&status_type=H&status_value=0" http://localhost:8000/devicestatus/

@author TKI
"""
def device_status(request): 
  # define default response
  response = { "error": "", "data": "" }
  # return if GET request
  if request.method == 'GET':
    response['error'] = {
      'no' : 'err0',
      'msg': 'sorry no gets'
    }
    return json_response_from(response)
  # params checking
  if not (request.POST.has_key('device_id') and request.POST.has_key('status_type') \
          and request.POST.has_key('status_value')): 
    response['error'] = {
      'no' : 'err1',
      'msg': 'missing mandatory params'
    }
    return json_response_from(response)
#  if not (request.POST['status_type'] == "O" and request.POST['status_value'] == "3" \
#          and request.POST.has_key('build_version')):
#    response['error'] = {
#      'no' : 'err1',
#      'msg': 'missing mandatory params'
#    }
#    return json_response_from(response)

  # data check
  try:
    dev = Device.objects.get(meid=request.POST['device_id'])
    #Heartbeat 
    if request.POST['status_type'] == "H":
      heartbeat = HeartbeatStatus(
        dev          = dev,
        status_value = request.POST['status_value'],
        timestamp    = datetime.now()
      )
      heartbeat.save()      
    #OTA 1: download completed, 2: signal before a phone goes into recovery, 3: build_version 
    if request.POST['status_type'] == "O":
      ota = OtaStatus()
      ota.dev = dev
      ota.status_value  = request.POST['status_value']
      ota.timestamp = datetime.now()
      if request.POST['status_value'] == "3":
        ota.build_version = request.POST['build_version']
      ota.save()      
  # device does not exist
  except Device.DoesNotExist:
    response['err'] = {
      'no' : 'err1',
      'msg': 'invalid device'
      }
    return json_response_from(response)
  
  # device
  response['data'] = dev.meid
  return json_response_from(response)


"""
Request_device 
@date 07/31/2012

@param number of devices
@return QuerySet of devices
@Usage: for obj in request_device("10"):
          do something
@author TKI
"""
def request_devices(number):
  #check a battery_load to calculate
  return DeviceProfile.objects.order_by('battery_load')[0:number]
