from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, render

from device.models import Device, DeviceApplication
from application.models import Application

from django.http import HttpResponse, HttpResponseRedirect
from lib.helper import json_response_from, json
from django.core.exceptions import ObjectDoesNotExist

"""
Index Transaction

@date 04/08/2012

@author TKI
"""
@login_required
#@permission_required
def index(request): 
  # get all users
  users = Transaction.objects.all

  return render_to_response(
            'transaction/index.html', 
            {
                'users': users
            },
            context_instance=RequestContext(request)
          )



"""
Index Transact Creation [POST]

@date 04/09/2012

@param device.id
@param app.id

@author TKI
"""
@login_required
#@permission_required
def create(request):



"""
Index Transact history

@date 04/09/2012

@author TKI
"""
@login_required
#@permission_required
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
    try:
      os.chdir(path)
      filelist = os.listdir(".")
      default.sort_nicely(filelist)
    except OSError, e:
      if e.errno != errno.EEXIST:
        response['err'] = {
          'no' : 'err1', 
          'msg': 'cannot change dir, failed upload'
        }
    
    return render_to_response(
  		'device/show.html', 
  		{
  			'device': device[0],
  			'filelist': filelist
  		},
      context_instance=RequestContext(request)
  	)
  # device does not exist
  else:
    response['err'] = {
      'no' : 'err1',
      'msg': 'invalid device'
    }
  return json_response_from(response)
