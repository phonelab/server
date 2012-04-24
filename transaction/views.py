from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, render

from django.contrib.auth.models import User
from device.models import Device, DeviceApplication
from application.models import Application
from transaction.models import Transaction, TransactionDevApp

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
  # get all transacts, devs, apps
  transacts = Transaction.objects.all()
  devs = Device.objects.all()
  apps = Application.objects.all()
  return render_to_response(
            'transaction/index.html', 
            {
                'transacts': transacts,
                'devs'     : devs,
                'apps'     : apps
            },
            context_instance=RequestContext(request)
          )

"""
Index Transact Creation [POST]

@date 04/09/2012

@param dev.id
@param app.id
@param action  0=install, 1=uninstall
ex) <QueryDict: {u'action': [u'0'], u'app': [u'1', u'2'], u'dev': [u'A000002A28021D', u'A000002A000000']}>

@author TKI
"""
@login_required
#@permission_required
def create(request):
  # define default response
  response = { "err": "", "data": "" }
  # return if GET request
  if request.method == 'GET':
    response['err'] = {
      'no' : 'err0',
      'msg': 'sorry no gets'
    }
    return HttpResponseRedirect('/error/')
  # params checking
  if not (request.POST.has_key('dev') and request.POST.has_key('app') \
          and request.POST.has_key('action')):
    response['error'] = {
      'no' : 'err1',
      'msg': 'missing mandatory params'
    }
    return json_response_from(response)

  dev_ids = request.POST.getlist('dev')
  app_ids = request.POST.getlist('app')
  transact = Transaction()
  transact.user = User.objects.get(id=request.POST['user'])
  transact.total = len(dev_ids) * len(app_ids)
  transact.progress = 0
  #transact.end = null

  #Check Data Validation
  for dev_id in dev_ids:
    for app_id in app_ids:
      #check FailureAlready(F1)
      if DeviceApplication.objects.filter(dev=dev_id).filter(app=app_id):
        if request.POST['action'] == "I":
          response['err'] = {
            'no' : 'err1',
            'msg': 'The application is already installed'
          }
          return json_response_from(response)
      #check FailureNoSuchApplication(F2)
      else:
        if request.POST['action'] == "U":  
          response['err'] = {
            'no' : 'err1',
            'msg': 'The phone does not have the application to uninstall'
          }
          return json_response_from(response)
    
  #insert the data from POST method
  for dev_id in dev_ids:
    for app_id in app_ids:
      transact.save()
      t_id = transact.id
      trndevapp = TransactionDevApp()
      trndevapp.tid = Transaction.objects.get(id=t_id)
      trndevapp.dev = Device.objects.get(id=dev_id)
      trndevapp.app = Application.objects.get(id=app_id)
      trndevapp.action = request.POST['action']
      trndevapp.result = "N" # N is N/A
      trndevapp.save()
      Device.objects.filter(id=dev_id).update(active="D")
#      Application.objects.filter(id=app_id).update(active="D")
  #send "new_manifest" message to phones via C2DM
  msg = "new_manifest"
  for dev_id in dev_ids:
    Device.objects.get(id=dev_id).send_message(payload=json({"message": msg}))
  return HttpResponseRedirect('/transaction/' + str(t_id) + '/1/')
  
  return json_response_from(response)


"""
Index Transact history

@date 04/09/2012

@author TKI
"""

@login_required
#@permission_required
#Id is userId or transId
def show(request, Id, Type): 
  # define default response
  response = { "err": "", "data": "" }
  # get transaction using userId or transId
  # get transactionDevapp using tid
  trans_list = {}
  if Type == "1":
    for o in Transaction.objects.filter(id=Id).values('id', 'user_id'):
      trans_list[o['id']] = o['user_id']
    id = Id
  else: 
    for o in Transaction.objects.filter(user=Id).values('id', 'user_id'):
      trans_list[o['id']] = o['user_id']
    id = User.objects.get(id=Id)
  
  transdevapps = TransactionDevApp.objects.filter(tid__in=trans_list.keys())
  return render_to_response(
    'transaction/show.html', 
    {
      'id'      : id,
      'transdevapps': transdevapps
    },
    context_instance=RequestContext(request)
  )

  return json_response_from(response)
