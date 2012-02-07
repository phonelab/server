from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render_to_response
from lib.helper import json_response_from

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
    return json_response_from(response)
  # Get Application/Experiment
  app = Application.objects.filter(id=appId)
  # if application exists, render download
  if app.count() == 1:
    return render(
    )
  else:
    response['err'] = {
      'no' : 'err1',
      'msg': 'application doesn`t exist'
    }

