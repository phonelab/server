from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from lib.helper import json_response_from
from django.conf import settings
from device.models import Application, DeviceApplication
import os, errno

RAW_APP_ROOT = settings.RAW_APP_ROOT

"""
Download experiment

@date 02/07/2012
@param String appId

@api public

@author Micheal
"""
def get_download(request, appId):
  # define default response
  response = { "err": "", "data": "" }
  # return if GET request
  if request.method == 'POST':
    response['err'] = {
      'no' : 'err0',
      'msg': 'sorry no POST'
    }
    return HttpResponseRedirect('/error/')
  # Get Application/Experiment
  app = Application.objects.filter(id=appId)
  # if application exists, render download
  if app.count() != 1:
    response['err'] = {
      'no' : 'err1',
      'msg': 'application doesn`t exist'
    }


"""
Show all Application

@date 03/19/2012

@author Micheal
"""
def index(request):
  # query the database for all applications
  apps = Application.objects.all

  return render_to_response(
      'application/index.html', 
      {
        'apps': apps
      }
    )


"""
Show Application Details [GET]

@date 03/20/2012
@param String appId

@author TKI
"""
def show(request, appId): 
  # define default response
  response = { "err": "", "data": "" }
  # get application
  app = Application.objects.filter(id=appId)
  # application exists
  if app.count() == 1:
    return render_to_response(
  		'application/show.html', 
  		{
  			'app': app[0],
  		}
  	)
  # application does not exist
  else:
    response['err'] = {
      'no' : 'err1',
      'msg': 'invalid application'
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
      #tagName = 'Battery_level'
      tagName = 'Battery level'
    elif statusType == '2':
      #tagName = 'Location_Latitude'
      tagName = 'Location: Latitude'
    else:
      #tagName = 'Signal_Strength'
      tagName = 'Signal Strength'
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
            Tagdata += ' [ ' + temp[0] + ' ' + temp[1] + ' ] '
            if statusType == '1':
              Tagdata += 'Battery Level: ' + temp[8]
            elif statusType == '2':
              Tagdata += 'GPS Latitude: ' + temp[8] + ', Longitude: ' + temp[10] + 'Accuracy: ' + temp[12]
            else:
              Tagdata += 'Signal Strengh: ' + temp[8] + ', asu: ' + temp[10]
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














"""
Upload Experiment Form

@date 03/19/2012

@author Micheal
"""
def new(request):
  app = Application()
  # query the database for all applications
  return render_to_response(
      'application/form.html', 
      {
        app: app
      }
    )

"""
Upload Application/Experiment Action

@date 03/05/2012

@author Micheal
"""
def create_or_update_application(request):
  # define default response
  response = { "err": "", "data": "" }
  # create new application
  if request.method == 'GET':
    response['err'] = {
      'no' : 'err0',
      'msg': 'sorry no GET'
    }
    return HttpResponseRedirect('/error/')
  else:
    # post 
    params = request.POST
    ## First Save to database
    app = Application(
        name          = params['name'], 
        package_name  = params['package_name'],
        intent_name   = params['intent_name'],
        description   = params['description'],
        type          = params['type'],
        version       = params["version"],
    )
    app.save()
    # Verify Filename is coming in post
    if (request.POST):
      filename = os.path.join(RAW_APP_ROOT, str(app.id) + ".apk")
      filedir = os.path.dirname(filename)
      # create folder for user if it doesn`t exist
      try:
        os.mkdir(filedir)
      except OSError, e:
        if e.errno != errno.EEXIST:
          print "some problem in creating dir"
          response['err'] = {
            'no' : 'err1', 
            'msg': 'cannot create dir, failed upload'
          }
          raise
      # get file handle
      fileHandle = open(filename, 'wb+')
      # write it out
      for chunk in request.FILES['upload'].chunks():
        print chunk
        fileHandle.write(chunk)
      # close file handle
      fileHandle.close()
      # success msg
      response['data'] = "done"
    else:
      response["err"] = "err1"
    print response["err"]
    return HttpResponseRedirect('/experiments/')
