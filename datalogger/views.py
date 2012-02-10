from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext
from django.utils import  simplejson as json
from device.models import Device
from lib.helper import json_response_from

import time
import os, errno
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
  # filename
  filename = os.path.join(RAW_LOG_ROOT, deviceId, str(int(time.time())) + ".log")
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
  # success msg
  response['data'] = "done"
  # render json response
  return json_response_from(response)


"""
Show Log for Device

@date 01/29/2012
@param String deviceId
@param String logFilename

@author Taeyeon
"""
def show(request, deviceId, logFilename):
	# define default response  
	response = { "err": "", "data": "" }  
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
				}
			)
		#the file does not exist
		else:
			response['err'] = {
				'no' : 'err1',
				'msg': 'No such log file'
			}
	#device does not exist		
	else:
		response['err'] = {
			'no' : 'err1',
			'msg': 'invalid device'
		}
	return json_response_from(response)
