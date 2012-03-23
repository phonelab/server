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
