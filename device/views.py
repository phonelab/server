from django.http import HttpResponse, HttpResponseRedirect
from device.models import Device, DeviceApplication
from django.shortcuts import render_to_response, render
from lib.helper import json_response_from
from django.conf import settings

import os, errno
import datetime

# Log Dir
RAW_LOG_ROOT = settings.RAW_LOG_ROOT

"""
List All Devices

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
Create New Device [POST]
Update Device Details [POST]

@date 01/29/2012
@param id IMEI number
@param email email
@param reg_id Registration Id

# Create new device
# curl -X POST -d "device_id=123&email=micheala@buffalo.edu&reg_id=some_id" http://107.20.190.88/device/

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
  if params['device_id'] == "" or params['reg_id'] == "":
    response['error'] = {
      'no' : 'err1',
      'msg': 'missing mandatory params'
    }
  # get device
  device = Device.objects.filter(id=params['device_id'])
  # if device exists, update
  if device.count() == 1:
    # email
    if (device.email != params['email']):
      device.email = params['email']
    # reg_id
    if (device.reg_id != params['reg_id']):
      device.reg_id = params['reg_id']
    # update
    if (device.update_interval != params['update_interval']):
      device.update_interval = params['update_interval']
    # save device
    device.save()
  # device does not exist, insert
  else:
    device = Device(
        id     = params['device_id'], 
        email  = "phonelab@gmail.com", #params['email'] 
        reg_id = params['reg_id']
    )
    # create device
    device.save()
    response['data'] = device
  # render json response
  return json_response_from(response)


"""
Show Device Details

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
    # try to change dir
    try:
      os.chdir(path) 
      filelist =  os.listdir(".")
    except OSError, e:
      if e.errno != errno.EEXIST:
        response['err'] = {
          'no' : 'err1', 
          'msg': 'cannot change dir, failed upload'
        }
        # TODO: report error
  	
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
Edit Device Form

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
Update Device

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
    return redirect('/error/')
  # get params from POST
  params = request.POST
  # get device
  device = Device.objects.filter(id=deviceId)
  # if device exists, update
  if device.count() == 1:
    #
    device = device[0]
    # email
    if (device.email != params['email']):
      device.email = params['email']
    # reg_id
    if (device.reg_id != params['reg_id']):
      device.reg_id = params['reg_id']
    # update
    if (device.update_interval != params['update_interval']):
      device.update_interval = params['update_interval']
    # save device
    device.save()
    # redirect to device/<deviceId>
    return HttpResponseRedirect('/device/' + device.id)
  # device does not exist
  else:
    return HttpResponseRedirect('/error/')
