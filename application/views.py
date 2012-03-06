from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render_to_response
from lib.helper import json_response_from
from django.conf import settings

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
Upload Application/Experiment Form

@date 03/05/2012

@api public

@author Micheal
"""
def new(request):
  # define default response
  response = { "err": "", "data": "" }
  # create new application
  if request.method == 'POST':
    response['err'] = {
      'no' : 'err0',
      'msg': 'sorry no POST'
    }
    return HttpResponseRedirect('/error/')
  else:
    return render_to_response(
      'application/form.html', 
      {

      }
    )

"""
Upload Application/Experiment Form

@date 03/05/2012

@api public

@author Micheal
"""
def new(request):
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
    destination = open(RAW_APP_ROOT, 'wb+')

    for chunk in request.FILES['upload'].chunks():
      destination.write(chunk)
    destination.close()

    return render_to_response(
      'application/form.html', 
      {

      }
    )