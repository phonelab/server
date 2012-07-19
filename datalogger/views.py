from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext
from django.utils import  simplejson as json
from device.models import Device, DeviceProfile
from lib.helper import json_response_from
from datetime import datetime
from utils import sort_nicely, is_valid_device
#import time
import os, errno, re
# Log Dir
RAW_LOG_ROOT = settings.RAW_LOG_ROOT

#
# TODO::
# need a better mechanism to tackle cross site forgery POST
#

"""
Upload File based on deviceId

@date 12/10/2011
@param String deviceId

@author Micheal
"""
def upload_log(request, deviceId):
  # return if GET request
  if request.method == 'GET':
    return HttpResponse(
      "Sorry Bub", 
      content_type='text/plain'
    )
  # define default response
  response = {"err": "", "data": ""}
  # Verify Filename is coming in post
  if ("filename" in request.POST):
    now = datetime.now()
    #filename = os.path.join(RAW_LOG_ROOT, deviceId, str(int(time.time())) + ".log")
    #filename = os.path.join(RAW_LOG_ROOT, deviceId, request.POST['filename'])
    filename = os.path.join(RAW_LOG_ROOT, deviceId, str(int(now.strftime("%Y%m%d%H%M"))) + ".log")
    filedir = os.path.dirname(filename)
    # create folder for user if it doesn`t exist
    try:
      print "trying to create dir" + str(filedir)
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
    for chunk in request.FILES['file'].chunks():
      fileHandle.write(chunk)
    # close file handle
    fileHandle.close()
    DeviceProfile.objects.filter(dev=deviceId).update(last_log=now)
    # success msg
    response['data'] = "done"
  else:
    response["err"] = "err1"

  # render json response
  return json_response_from(response)


"""
Show Log for Device

@date 01/29/2012
@param String deviceId
@param String logFilename

@author Taeyeon
"""
@login_required
def show(request, deviceId, logFilename):
  user = request.user
  # define default response  
  response = { "err": "", "data": "" }  

  if is_valid_device(user, deviceId):
    # get device  
    device = Device.objects.filter(id=deviceId)
    # if device exists, update  
    if device.count() == 1:
      # generate file name    
      filename = os.path.join(RAW_LOG_ROOT, deviceId, logFilename + ".log")		
      if os.path.isfile(filename):			
        # open log file
        Logfile = open(filename, 'r+')
        # read file
        Logdata = Logfile.read()
        # render respone
        return render_to_response(
          'device/log.html',
          {
            'device': device[0],
            'logFilename': logFilename,
            'Logdata': Logdata
          },
          context_instance=RequestContext(request)
        )
      #the file does not exist 
      else:
        response['err'] = {
          'no' : 'err2',
          'msg': 'No such log file'
        }
    #device does not exist		
    else:
      response['err'] = {
        'no' : 'err1',
        'msg': 'invalid device'
      }
    return json_response_from(response)
  else:
    return HttpResponseRedirect('/')



"""
Log Tag filter

@date 02/16/2012
@param String deviceId
@param String tagName

@author Taeyeon
"""
@login_required
def show_tag(request, deviceId):
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
      sort_nicely(filelist)
      Tagdata = ''
      for file in filelist:
        filename = os.path.join(RAW_LOG_ROOT, deviceId, file)
        Logfile = open(filename, 'r+')
        for line in Logfile:
          #Logdata = Logfile.readline()
          #Two ways to find with string and without string
          if re.search(request.POST['tagName'], line):
            if not request.POST.has_key('anti'):
              Tagdata += line
          else:
            if request.POST.has_key('anti'):
              Tagdata += line
        
      # render respone
      return render_to_response(
        'device/filter.html',
        {
          'device': device[0],
          'TagName': request.POST['tagName'],
          'Tagdata': Tagdata
        },
        context_instance=RequestContext(request)
      )
      Logfile.close()
      Tagfile.close()
    except OSError, e:
      if e.errno != errno.EEXIST:
        response['err'] = {
          'no' : 'err2', 
          'msg': 'cannot change dir'
        }
    
  else:
    response['err'] = {
      'no' : 'err1',
      'msg': 'invalid device'
    }
  return json_response_from(response)
