from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext
from django.utils import  simplejson as json

import time
import os, errno

RAW_LOG_ROOT = os.path.join(settings.SITE_ROOT, 'datalogger', 'logs')

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
def upload_file(request, deviceId):
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
