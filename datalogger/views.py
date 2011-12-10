from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.template import RequestContext
from django.utils import  simplejson as json

import time
import os

RAW_LOG_ROOT = os.path.join(settings.SITE_ROOT, 'datalogger', 'logs')

def handle_uploaded_file(f):
  destination = open('log', 'wb+')
  for chunk in f.chunks():
    destination.write(chunk)
  destination.close()

#
# TODO::
# need a better mechanism to tackle cross site forgery POST
#

@csrf_exempt
def upload_file(request, deviceId):
  err = ""
  msg = ""

  # if request is post
  if request.method == 'POST':
    print request.POST
    print request.FILES
    # filename
    filename = os.path.join(RAW_LOG_ROOT, deviceId, str(int(time.time())) + ".log")
    dir = os.path.dirname(filename)
    # create folder for user if it doesn`t exist
    try:
      print "trying to create dir"
      os.mkdir(dir)
    except OSError, e:
      if e.errno != errno.EEXIST:
        print "some problem in creating dir"
        err = "err1"
        msg = "cannot create dir, failed upload"
        raise
        
    # open file
    fileHandle = open(filename, 'wb+')
    # write it out
    for chunk in request.FILES['file'].chunks():
      fileHandle.write(chunk)
    fileHandle.close()

    # success msg
    msg = "done"

  else:
    print request.GET
    logfile = LogFile(
      logFile = request.GET.get('logfile', ''),
      deviceId = deviceIddeviceId, 
    )
  return HttpResponse(json.dumps({err: err, msg: msg}), mimetype='application/json')
