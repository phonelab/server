from django.http import HttpResponse
from device.models import Device, DeviceApplication
from django.shortcuts import render_to_response, render
from lib.helper import json_response_from

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
# curl -X POST -d "id=123&email=micheala@buffalo.edu&reg_id=some_id" http://127.0.0.1:8000/device/

@author Micheal
"""
def create_device(request): 
  # define default response
  response = { "err": "", "data": "" }
  # return if GET request
  if request.method == 'GET':
    response['err'] = {
      'no' : 'err0',
      'msg': 'sorry no gets'
    }
    return json_response_from(response)
  # get params from POST
  params = request.POST
  # error checking
  if params['id'] == "" or params['reg_id'] == "":
    response['err'] = {
      'no' : 'err1',
      'msg': 'missing mandatory params'
    }
    return json_response_from(response)
  # get device
  device = Device.objects.filter(id=params['id'])
  # if device exists, update
  if device.count() == 1:
    if (device.email != params['email']):
      device.email = params['email']
    if (device.reg_id != params['reg_id']):
      device.reg_id = params['reg_id']
      # get new token from goog servers
    
    # save if changed, else let it b

  # device does not exist, insert
  else:
    device = Device(
        id     = params['id'], 
        email  = params['email'], 
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
    device = device[0]
    # TODO get logs for that particular device
    response['data'] = device
  # device does not exist
  else:
    response['err'] = {
      'no' : 'err1',
      'msg': 'invalid device'
    }

  return json_response_from(response)
