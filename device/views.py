from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from device.forms import *
from django.template import RequestContext
#from django.contrib.auth.models import User

from django.http import HttpResponse, HttpResponseRedirect
from device.models import Device, DeviceApplication
from django.shortcuts import render_to_response, render
from lib.helper import json_response_from, json
from django.conf import settings
import default
import os, errno, re
import datetime
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
           'main_page.html',
           { 'user': request.user},
           context_instance=RequestContext(request)
         )

def logout_page(request):
  logout(request)
  return HttpResponseRedirect('/')

def register_page(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      user = User.objects.create_user(
        username=form.cleaned_data['username'],
        password=form.cleaned_data['password1'],
        email=form.cleaned_data['email']
      )
      return HttpResponseRedirect('/')
  else:
    form = RegistrationForm()
  return render_to_response(
           'registration/register.html',
           { 'form': form },
           context_instance=RequestContext(request)
         )

"""
List All Devices

@date 02/07/2012

@author Micheal
"""
@login_required
#@login_required(login_url='/login/')
def index(request): 
  # get all devices
  devices = Device.objects.all

  return render_to_response(
            'device/index.html', 
            {
                'devices': devices
            },
            context_instance=RequestContext(request)
          )

"""
Create New Device [POST]
Update Device Details [POST]

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
  device = Device.objects.filter(id=params['device_id'])
  # if device exists, update
  if device.count() == 1:
    device = device[0]
    # email
    if ('email' in params and device.email != params['email']):
      device.email = params['email']
    # reg_id
    if ('reg_id' in params and device.reg_id != params['reg_id']):
      device.reg_id = params['reg_id']
    # update
    if ('update_interval' in params and device.update_interval != params['update_interval']):
      device.update_interval = params['update_interval']
  # device does not exist, insert
  else:
    device = Device(
        id     = params['device_id'], 
        email  = "phonelab@gmail.com", #params['email'] 
        reg_id = params['reg_id']
    )
  # save device
  device.save()
  # device
  response['data'] = device
  # render json response
  return json_response_from(response)


"""
List All Devices [GET]

@date 02/07/2012

@author Micheal
"""
def index(request): 
  # get all devices
  devices = Device.objects.all

  return render_to_response(
            'device/index.html', 
            {
                'devices': devices
            }
          )

"""
Show Device Details [GET]

@date 01/29/2012
@param String deviceId

@author Micheal
"""
def show(request, deviceId): 
  # define default response
  response = { "err": "", "data": "" }
  # get device
  device = Device.objects.filter(id=deviceId)
  # device exists
  if device.count() == 1:
    # get log data list from deviceId directory
    path = os.path.join(RAW_LOG_ROOT, device[0].id)
    # empty
    filelist = {}
    try:
      os.chdir(path)
      filelist = os.listdir(".")
      default.sort_nicely(filelist)
    except OSError, e:
      if e.errno != errno.EEXIST:
        response['err'] = {
          'no' : 'err1', 
          'msg': 'cannot change dir, failed upload'
        }
    
    return render_to_response(
  		'device/show.html', 
  		{
  			'device': device[0],
  			'filelist': filelist
  		}
  	)
  # device does not exist
  else:
    response['err'] = {
      'no' : 'err1',
      'msg': 'invalid device'
    }
  return json_response_from(response)


"""
Edit Device Form [GET]

@date 02/08/2012
@param String deviceId

@author Micheal
"""
def edit(request, deviceId):
  # define default response
  response = { "err": "", "data": "" }
  # get device
  device = Device.objects.filter(id=deviceId)
  # device exists
  if device.count() == 1:
    return render_to_response(
      'device/edit.html', 
        {
          'device': device[0]
        }
      )
  # device does not exist
  else:
    response['err'] = {
      'no' : 'err1',
      'msg': 'invalid device'
    }
    return HttpResponseRedirect('/error/')

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
    if ('email' in params and device.email != params['email']):
      device.email = params['email']
    # reg_id
    if ('reg_id' in params and device.reg_id != params['reg_id']):
      device.reg_id = params['reg_id']
    # update
    if ('update_interval' in params and device.update_interval != params['update_interval']):
      device.update_interval = params['update_interval']
    # save device
    device.save()
    # redirect to device/<deviceId>
    return HttpResponseRedirect('/device/' + device.id)
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
    device = Device.objects.filter(id=deviceId)
    # if device exists, update
    if device.count() == 1:
      response = device[0].send_message(payload=json({"message": msg}))
    else:
      return HttpResponseRedirect('/error/')
  return json_response_from(response)		


"""
Status monitor [GET]

@date 02/20/2012
@param String deviceId
@param String statusType

@author Taeyeon
"""
def status(request, deviceId, statusType):
  # define default response
  response = { "err": "", "data": "" }
  # get device
  device = Device.objects.filter(id=deviceId)
  # device exists

  if device.count() == 1:
    # get log data list from deviceId directory
    path = os.path.join(RAW_LOG_ROOT, device[0].id)
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
      default.sort_nicely(filelist)
      Tagdata = ''
      for file in filelist:
        filename = os.path.join(RAW_LOG_ROOT, deviceId, file)
        Logfile = open(filename, 'r+')
        for line in Logfile:
          #Logdata = Logfile.readline()
          if re.search(tagName, line):
            temp = line.split(" ")
            print temp
            Tagdata += ' [ ' + temp[0] + ' ' + temp[1] + ' ] '
            if statusType == '1':
              Tagdata += 'Battery Level: ' + temp[9]
            elif statusType == '2':
              Tagdata += 'GPS Latitude: ' + temp[9] + ', Longitude: ' + temp[11] + 'Accuracy: ' + temp[13]
            else:
              Tagdata += 'Signal Strengh: ' + temp[9] + ', asu: ' + temp[11]
      # render respone
      return render_to_response(
        'device/status.html',
        {
          'device': device[0],
          'TagName': tagName,
          'Tagdata': Tagdata
        }
      )
      Logfile.close()
      Tagfile.close()
    except OSError, e:
      if e.errno != errno.EEXIST:
        response['err'] = {
          'no' : 'err1', 
          'msg': 'cannot change dir'
        }
    
    return render_to_response(
  		'device/show.html', 
  		{
  			'device': device[0],
  			'filelist': filelist
  		}
  	)
  # device does not exist
  else:
    response['err'] = {
      'no' : 'err1',
      'msg': 'invalid device'
    }
  return json_response_from(response)
