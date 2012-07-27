from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.servers.basehttp import FileWrapper
from django.utils.encoding import smart_str
from django.shortcuts import render_to_response
from lib.helper import json_response_from
from django.conf import settings
from device.models import Device, DeviceApplication, DeviceProfile
from application.models import Application
from experiment.models import Experiment
from users.models import UserProfile
from xml.etree import ElementTree
import os, errno, mimetypes
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
  path = os.path.join(RAW_APP_ROOT, str(app[0].id) + ".apk")
  wrapper = FileWrapper(open(path, "r"))
  content_type = mimetypes.guess_type(path)[0]
  response = HttpResponse(wrapper, content_type = content_type) 
  response['Content-Length'] = os.path.getsize(path)
  response['Content-Disposition'] = 'attachment; filename=%s' %smart_str(os.path.basename(path))
  return response
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
"""
Show Application corresponding to user type

@date 07/02/2012

@author Manoj
"""
@login_required
def index(request):
  user = request.user
  userprofile = UserProfile.objects.get(user_id=user.id)

  apps = {} 
  if userprofile.user_type == 'P':
    # query the database for all applications
    apps = Application.objects.all().order_by('-created')
    
  elif userprofile.user_type == 'E':
    #query the database for user's own applications
    apps = Application.objects.filter(user=user)

  elif userprofile.user_type == 'A':
    apps = Application.objects.all().order_by('-created')

  return render_to_response(
      'application/index.html', 
      { 
#       'group': userprofile.group,
        'apps': apps,
        'userprofile': userprofile
      },
      context_instance=RequestContext(request)
    )


"""
Show Application Details [GET]

@date 03/20/2012
@param String appId

@author TKI
"""
@login_required
def show(request, appId): 
  userprofile = UserProfile.objects.get(user=request.user)
  # define default response
  response = { "err": "", "data": "" }
  # get application
  devs = {}
  try:
    app = Application.objects.get(id=appId)
    # application exists
    for o in DeviceApplication.objects.filter(app=app):
      for dev in Device.objects.filter(id=o.dev.id):
        devs[dev] = dev

    return render_to_response(
  		'application/show.html', 
  		{
        'group': userprofile.group,
        'userprofile': userprofile,
  			'app' : app,
        'devs': devs
  		},
      context_instance=RequestContext(request)
  	)
  # application does not exist
  except Application.DoesNotExist:
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
@login_required
def new(request):
  app = Application()
  # query the database for all applications
  return render_to_response(
      'application/form.html', 
      {
        'app': app
      },
      context_instance=RequestContext(request)
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
        user          = request.user,
        name          = params['name'], 
        #package_name = params['package_name'],
        #intent_name  = params['intent_name'],
        description   = params['description'],
        type          = params['type'],
        active        = "E"
        #version      = params["version"],
    )
    userprofile = UserProfile.objects.get(user = request.user)
    if userprofile.user_type=='E':
      app.group = userprofile.group
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
#        print chunk
        fileHandle.write(chunk)
      # close file handle
      fileHandle.close()
      #pulling package name from apk file
      #apktool extract apk file to a directory
#      os.system('bin/apktool d ' + filename)
#      with open(str(app.id) + '/AndroidManifest.xml', 'rt') as f:
#        tree = ElementTree.parse(f)
#      for node in tree.iter('manifest'):
#        package = node.attrib.get('package')
#      Application.objects.filter(id=app.id).update(package_name=package)
      #remove the directory 
#      os.system('rm -rf ' + str(app.id))
      # success msg
      response['data'] = "done"
    else:
      response["err"] = "err1"
#    print response["err"]
    return HttpResponseRedirect('/applications/')


"""
Withdraw an Application

@date 07/09/2012

@author Manoj
"""
def withdraw(request, appId):
  user = request.user
  userprofile = UserProfile.objects.get(user_id=user.id)
  
  app = Application.objects.get(id = appId)
  app.delete()

  apps = Application.objects.filter(user_id=user.id)

  return render_to_response(
      'application/index.html', 
      {
        'apps': apps,
        'user_type': userprofile.user_type
      },
      context_instance=RequestContext(request)
    )
