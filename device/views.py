from django.http import HttpResponse
from device.models import Device, DeviceApplication
from django.shortcuts import render_to_response
from lib.helper import json_response_from

"""
Create New Device [POST]

@date 01/29/2012
@param id IMEI number
@param email email
@param reg_id Registration Id

# Create new device
# curl -X POST -d "id=123&email=micheala@buffalo.edu&reg_id=some_id" http://127.0.0.1:8000/device/

@author Micheal
"""
def create(request): 
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
  # device exists
  if device.count() == 1:
    response['err'] = {
      'no' : 'err2',
      'msg': 'device already exists'
    }
  # device does not exist
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
Update Device Details

@date 02/01/2012
@param String deviceId

# curl -X http://127.0.0.1:3000/device/

@author Micheal
"""
def update(request, deviceId):


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