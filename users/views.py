from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import send_mail
from django.template import RequestContext, Context, loader
from django.http import HttpResponseRedirect
from django.contrib.sites.models import Site
from datetime import datetime, timedelta
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from django import forms
import random, hashlib, os, errno, mimetypes, re
from settings import FROM_EMAIL, ADMINS
#from django.utils import  simplejson as json
from lib.helper import json_response_from, json
from users.models import UserProfile, Participant, ParticipantRegister
from device.models import Device, DeviceProfile, StatusMonitor
from users.forms import RegistrationForm, ParticipantForm, ParticipantRegisterForm
from application.models import Application
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.encoding import smart_str
from experiment.models import Experiment
from django.conf import settings

RAW_AGREEMENT_ROOT = settings.RAW_AGREEMENT_ROOT
RAW_LOOKUP_ROOT = settings.RAW_LOOKUP_ROOT

admin_mail = 'tempphonelab@gmail.com'

#TO = [ email for name, email in ADMINS ]


"""
Detailed information for Participants

@date 08/07/2012/

@author Manoj
"""
def info(request):
  return render_to_response(
          'info.html',
          context_instance = RequestContext(request)
         )


"""
Participant Register and Device Register

@date 08/13/2012

@author TKI
"""
def participant_register(request):
  if request.user.is_superuser:
    if request.method == 'POST':
      form = ParticipantRegisterForm(request.POST)
      if form.is_valid():
        path = os.path.join(RAW_LOOKUP_ROOT, 'phonelab.txt')
        f = open(path, 'r') 
        for line in f:
          if re.search(form.cleaned_data['lib_number'], line):
            # result[0]: lib_number, 1: person number, 2:ub_id, 3: last_name, 4: first_name
            result = line.split(' ,')
            info = {'ub_id': result[2].strip(), 'email': result[2].strip()+'@buffalo.edu', 'last_name': result[3].strip(), 'first_name': result[4].strip()}
            break
          else:
            info = {}

        return render_to_response (
                 'participant_register_form.html',
                 {
                 'preview': True,
                 'form': form.cleaned_data,
                 'info': info
                 },
                 context_instance=RequestContext(request)
              )

      else: 
        form = ParticipantRegisterForm(request.POST)
        return render_to_response(
                 'participant_register_form.html',
                 {'form': form},
                 context_instance=RequestContext(request)
               )

    else:
      form = ParticipantRegisterForm()
      return render_to_response(
               'participant_register_form.html',
               {'form': form},
               context_instance=RequestContext(request)
             )
  else:
    return HttpResponseRedirect('/')  

def confirm_participant_register(request):
  # params checking
  if (request.POST['ub_id'] == '' and request.POST['email'] == '' \
         and request.POST['first_name'] =='' and request.POST['last_name'] ==''):
    participantregister = ParticipantRegister(
                         lib_number = request.POST['lib_number'],
                         meid       = request.POST['meid']
                         )
    participantregister.save()
    return render_to_response(
    	'participant_register_form.html',
      {
      'success': True,
      },
      context_instance=RequestContext(request)
      )
  else:
    password = User.objects.make_random_password(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
    user = User.objects.create_user(request.POST['ub_id'], request.POST['email'], password)
    user.is_active = False
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.save() 
	
    # Build the activation key for their account                                                                                                                    
    salt = hashlib.md5(str(random.random())).hexdigest()[:5]
    activation_key = hashlib.md5(salt+user.username).hexdigest()
    key_expires = datetime.today() + timedelta(2)
    userprofile = UserProfile(
                user = user,
                user_type = "P",
                activation_key=activation_key, 
                key_expires=key_expires
                )
    # Create and save their profile                                                                                                                                 
    userprofile.save()

    device = Device(
           meid = request.POST['meid'],
           active = "E"
           )
    device_id = device.save()
    device.save()
  
    # create monitor interval in StatusMonitor class
    statusmonitor = StatusMonitor(
                  name = 'monitorInterval',
                  value = '10',
                  units = 'min')
    statusmonitor.save()
  
    # Create and save device profile
    deviceprofile = DeviceProfile()
    deviceprofile.dev = device
    deviceprofile.user = user
    #deviceprofile.phone_no = request.POST['phone_number']
    deviceprofile.status = "W"
    #deviceprofile.purpose = ""
    if request.POST['meid'].startswith('A0000', 0, 5):
       deviceprofile.service_type = "4"
    else:
       deviceprofile.service_type = "3"
    deviceprofile.save()
    deviceprofile.statusmonitor.add(statusmonitor)
    deviceprofile.save()
    return render_to_response(
    	'participant_register_form.html',
      {
      'success': True,
      },
      context_instance=RequestContext(request)
      )

"""
Download Participant Agreement

@date 08/10/2012

@author Manoj
"""
def download_agreement(request):
  path = os.path.join(RAW_AGREEMENT_ROOT, 'information.pdf')

  wrapper = FileWrapper(open(path, "r"))
  content_type = mimetypes.guess_type(path)[0]
  response = HttpResponse(wrapper, content_type = content_type) 
  response['Content-Length'] = os.path.getsize(path)
  response['Content-Disposition'] = 'attachment; filename=%s' %smart_str(os.path.basename(path))
  return response


"""
Participant Email List

@date 07/23/2012

@author Manoj
"""

def participant(request):

  if request.method == 'POST':
    #Bind ParticipantForm with the request
    form = ParticipantForm(request.POST)
    if form.is_valid():
      #Save the Participant information
      participant = Participant(
                  name = form.cleaned_data['name'],
                  email = form.cleaned_data['email'],
                  student_status = form.cleaned_data['student_status'],
                  submitted_time = datetime.now()
      )
      exp_year = '20'+form.cleaned_data['expected_grad_year']
      exp_month = form.cleaned_data['expected_grad_month']
      expected_grad = exp_year+'-'+exp_month+'-01'
      participant.expected_grad = expected_grad
      participant.save()

      return render_to_response (
               'participant_interest_form.html',
               {
               'success': True
               },
               context_instance=RequestContext(request)
               )

    else: 
     #if form is invalid
     form = ParticipantForm(request.POST)
     return render_to_response(
              'participant_interest_form.html',
              {'form': form},
              context_instance=RequestContext(request)
              )

  else:
    form = ParticipantForm()
    return render_to_response(
            'participant_interest_form.html',
            {'form': form},
            context_instance=RequestContext(request)
            )      


"""
Register New User with activation

@date 05/09/2010

@author TKI
"""
def register(request):

  if request.user.is_authenticated():
  # They already have an account; don't let them register again
    return render_to_response(
             'users/register.html', 
             {'has_account': True},
             context_instance=RequestContext(request)
           )

  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid(): 
      # Find the user type
      user = form.save(form)
      user_type = form.cleaned_data['user_type']
      # Build the activation key for their account                                                                                                                    
      salt = hashlib.md5(str(random.random())).hexdigest()[:5]
      activation_key = hashlib.md5(salt+user.username).hexdigest()
      key_expires = datetime.today() + timedelta(2)
      new_profile = UserProfile(user=user, activation_key=activation_key, key_expires=key_expires, user_type = user_type)
      current_site = Site.objects.get_current()
 
      EMAIL_SUBJECT = 'Phonelab Email Verification'
      c = Context({'user': user, 'key': new_profile.activation_key, 'site_name': current_site})
      EMAIL_BODY = (loader.get_template('users/mails/user_signup.txt')).render(c)
      TO_EMAIL = [user.email]
      send_mail(EMAIL_SUBJECT, EMAIL_BODY, FROM_EMAIL, TO_EMAIL)
      
      # Create and save their profile                                                                                                                                 
      new_profile.save()
        
      return render_to_response(
              'users/register.html',
              { 'created': True,
              'user_type': user_type,
              'mail'   : user.email },
              context_instance=RequestContext(request)
            )


      
  else:
    form = RegistrationForm()
       
  return render_to_response(
           'users/register.html',
           { 'form': form },
           context_instance=RequestContext(request)
         )


"""
Email activation 

@param: activation_key
@date 05/18/2010
@author TKI
"""

def confirm(request, activation_key):
  
  if request.user.is_authenticated():
    return render_to_response(
             'users/confirm.html', 
             {'has_account': True},
             context_instance=RequestContext(request)
           )
  
  userprofile = get_object_or_404(UserProfile, activation_key=activation_key)
  if userprofile.key_expires < datetime.today():
    return render_to_response(
             'users/confirm.html', 
             {'expired': True},
             context_instance=RequestContext(request)
           )

  userprofile.user.is_active = True
  userprofile.user.save()
  return render_to_response(
          'users/confirm.html', 
          {'activated': True,},
          context_instance=RequestContext(request)
         )
  


"""
User Profile

@date 05/21/2010

@author TKI

@date 07/17/2012

Updated to include experiment tab

@author Manoj

"""
@login_required
def profile(request):
  
  experiments = {}

  # define default response
  response = {"err": "", "data": ""}
  try:
    # get UserProfile with user foreignkey
    userprofile = UserProfile.objects.get(user=request.user)

    if userprofile.user_type == 'A':
      #get all devices
      devprofiles = DeviceProfile.objects.all()

    #get Experiment details if experimenter
    if(userprofile.user_type== 'E'):

      experiments = Experiment.objects.filter(user=request.user)
      
    return render_to_response(
             'users/profile.html', 
             { 'userprofile' : userprofile,
               'experiments': experiments },
             context_instance=RequestContext(request)
             )
  
  # User does not exist
  except UserProfile.DoesNotExist: 
    response['err'] = {
      'no' : 'err1',
      'msg': 'invalid user'
    }
  return json_response_from(response)


"""
Update User Profile Via Form [POST]

@date 05/21/2012

@param String userId

@author Micheal
"""
def update(request, userId):
  # define default response
  response = { "err": "", "data": "" }
  # return if GET request
  if request.method == 'GET':
    response['err'] = {
      'no' : 'err0',
      'msg': 'sorry no gets'
    }
    return HttpResponseRedirect('/error/')
  # get params from POST
  params = request.POST
  try:
    # get UserProfile with user foreignkey
    userprofile = UserProfile.objects.get(user=userId)    
    user = User.objects.get(id=userId)    
    # User First Name
    if ('fname' in params and userprofile.user.first_name != params['fname']):
      user.first_name = params['fname']
    # User Last Name
    if ('lname' in params and userprofile.user.last_name != params['lname']):
      user.last_name = params['lname']
    # User email, not device email
    if ('email' in params and userprofile.user.email != params['email']):
      user.email = params['email']
    # save User and UserProfile
    user.save()
    userprofile.save()
    # redirect to /accounts/profile/userId
    return HttpResponseRedirect('/accounts/profile/')
# User does not exist
  except User.DoesNotExist: 
    response['err'] = {
      'no' : 'err1',
      'msg': 'invalid user'
    }
  return json_response_from(response)


def is_member(user, deviceId):
  if user:
    return UserProfile.objects.filter(user=user).filter(user_type="M").count() > 0
  return False

def is_leader(user):
  if user:
    return UserProfile.objects.filter(user=user).filter(user_type="L").count() > 0
  return False



###Group Authorization
# """
# Email Authorization

# @date 07/03/2012

# @params String groupname,
#         activation_key
        

# @author Manoj
# """

# def authorize(request, groupname, activation_key):
#   user_profile = get_object_or_404(UserProfile, activation_key=activation_key)
#   user = user_profile.user

#   #Account already activated 
#   if user.is_active:
#     return render_to_response(
#              'users/confirm.html', 
#              {'has_account': True,
#               'req_user': user},
#              context_instance=RequestContext(request)
#            )
  
#   #Key Expired 
#   if user_profile.key_expires < datetime.today():
#     return render_to_response(
#              'users/confirm.html', 
#              {'expired': True},
#              context_instance=RequestContext(request)
#            )

  
#   elif user_profile.user_type == 'L':
#     group = Group.objects.create(name=groupname)
#     user.groups = [group]
#     user_profile.group = group
#     user_profile.save()
#     EMAIL_SUBJECT = 'Phonelab Admin Authorization'

#   elif user_profile.user_type=='M':
#     group = Group.objects.get(name=groupname)
#     user.groups = [group]
#     user_profile.group = group
#     user_profile.save()
#     EMAIL_SUBJECT = 'Phonelab Leader Authorization'
    
#   current_site = Site.objects.get_current()
#   c = Context({'user': user, 'group': group ,'user_type': user_profile.user_type, 'key': activation_key, 'site_name': current_site})
#   EMAIL_BODY = (loader.get_template('users/mails/user_signup.txt')).render(c)
#   TO_EMAIL = [user.email]
#   send_mail(EMAIL_SUBJECT, EMAIL_BODY, FROM_EMAIL, TO_EMAIL)

#   return render_to_response(
#           'users/confirm.html', 
#           {'success': True,
#            'user_type': user_profile.user_type,
#            'req_user': user},
#             context_instance=RequestContext(request)
#          )


# """
# Group Profile

# @date 07/16/2012

# @param String groupname

# @author Manoj
# """

# def group_profile(request):

#   #initialize beeloan
#   device_requested = False

#   user = request.user
#   userprofile = UserProfile.objects.get(user=user)

#   #get the group
#   group = Group.objects.get(user = user)

#   #get the devices and number of devices
#   devices = DeviceProfile.objects.filter(group=group)
#   no_of_devices = devices.count()

  
#   #get the leader
#   leader = get_object_or_404(UserProfile, user_type='L', group=group)

#   #get the apps
#   apps = Application.objects.filter(group=userprofile.group)

#   #get the members
#   members = UserProfile.objects.filter(user_type='M', group=group)

#   if request.POST:
#     params = request.POST

#     if 'req_devices' in params:
#       req_devices = params['req_devices']

#       current_site = Site.objects.get_current()
#       c = Context({'leader': leader.user, 'group': group ,'req_devices': req_devices, 'available_devices': no_of_devices, 'site_name': current_site})
#       EMAIL_SUBJECT = "Group "+group.name+" Device request"
#       EMAIL_BODY = (loader.get_template('users/mails/device_request.txt')).render(c)
#       TO_EMAIL = [admin_mail]
#       send_mail(EMAIL_SUBJECT, EMAIL_BODY, FROM_EMAIL, TO_EMAIL)

#       device_requested = True

#   return render_to_response(
#           'users/group_profile.html', 
#              { 'device_requested': device_requested,
#                'userprofile' : userprofile,
#                'group': group,
#                'apps': apps,
#                'leader': leader,
#                'members': members,
#                'no_of_devices': no_of_devices, 
#                'devices'  : devices },
#              context_instance=RequestContext(request)
#          )


###Part of Groups
# """
# Delete member from group

# @date 07/16/2012

# @param String member

# @author Manoj
# """
# def delete_member(request, member):
  
#   group_member = User.objects.get(username=member)
#   member_profile = UserProfile.objects.get(user = group_member)
#   group = Group.objects.get(user = group_member)

#   #remove the user from group
#   group_member.groups.remove(group)

#   #Update userprofile
#   member_profile.group_id = ""
#   member_profile.user_type = "P"
  

#   user = request.user
#   userprofile = UserProfile.objects.get(user=user)

#   #Notify the member
#   current_site = Site.objects.get_current()
#   c = Context({'user': group_member, 'group': group ,'leader': user, 'site_name': current_site})
#   EMAIL_SUBJECT = "Phonelab: Group "+group.name+" Notification"
#   EMAIL_BODY = (loader.get_template('users/mails/member_removed.txt')).render(c)
#   TO_EMAIL = [member_profile.user.email]
#   send_mail(EMAIL_SUBJECT, EMAIL_BODY, FROM_EMAIL, TO_EMAIL)

#   member_profile.save()

#   return HttpResponseRedirect('/accounts/group_profile/')

# usage: @user_passes_test(is_leader, login_url='/login')
# usage: @user_passes_test(is_member, login_url='/login')

