from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import send_mail
from django.template import RequestContext, Context, loader
from django.http import HttpResponseRedirect
from django.contrib.sites.models import Site

from settings import FROM_EMAIL, ADMINS
#from django.utils import  simplejson as json
from lib.helper import json_response_from, json
from django.contrib.auth.models import User, Group
from users.models import UserProfile
from device.models import Device, DeviceProfile
from users.forms import RegistrationForm
import datetime, random, hashlib
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django import forms

admin_mail = 'tempphonelab@gmail.com'

#TO = [ email for name, email in ADMINS ]
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
      user_type = form.cleaned_data['user_type']
      
      if(user_type=='L'):
        groupname = form.cleaned_data['groupname']
        user = form.save(form)
        # Build the activation key for their account                                                                                                                    
        salt = hashlib.md5(str(random.random())).hexdigest()[:5]
        activation_key = hashlib.md5(salt+user.username).hexdigest()
        key_expires = datetime.datetime.today() + datetime.timedelta(2)
        new_profile = UserProfile(user=user, activation_key=activation_key, key_expires=key_expires, user_type = user_type)
        current_site = Site.objects.get_current()
 
        EMAIL_SUBJECT = 'Signup Authorization for an experiment Leader'
        c = Context({'user': user.username, 'group': groupname, 'email':user.email, 'key': new_profile.activation_key, 'site_name': current_site})
        EMAIL_BODY = (loader.get_template('users/mails/leader_request.txt')).render(c)
        TO_EMAIL = [admin_mail]
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


      elif(user_type=='M'):
        

        # Experiment leader name
        group = form.cleaned_data['groupname']
        leader_profile = get_object_or_404(UserProfile, group=group, user_type='L' )
        leader = leader_profile.user
        user = form.save(form)
        # Build the activation key for their account                                                                                                                    
        salt = hashlib.md5(str(random.random())).hexdigest()[:5]
        activation_key = hashlib.md5(salt+user.username).hexdigest()
        key_expires = datetime.datetime.today() + datetime.timedelta(2)
        new_profile = UserProfile(user=user, activation_key=activation_key, key_expires=key_expires, user_type = user_type)
        current_site = Site.objects.get_current()

        EMAIL_SUBJECT = 'Phonelab: Member request for '+ group.name
        c = Context({'user': user.username, 'email':user.email, 'group': group.name, 'leader_name':leader.username, 'key': new_profile.activation_key, 'site_name': current_site})
        EMAIL_BODY = (loader.get_template('users/mails/member_request.txt')).render(c)
        TO_EMAIL = [leader.email]
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
Email Authorization

@date 07/03/2012

@author Manoj
"""

def authorize(request, groupname, activation_key):
  user_profile = get_object_or_404(UserProfile, activation_key=activation_key)
  user = user_profile.user

  if user.is_active:
    return render_to_response(
             'users/confirm.html', 
             {'has_account': True,
              'req_user': user},
             context_instance=RequestContext(request)
           )
  
  if user_profile.key_expires < datetime.datetime.today():
    return render_to_response(
             'users/confirm.html', 
             {'expired': True},
             context_instance=RequestContext(request)
           )

  
  elif user_profile.user_type == 'L':
    group = Group.objects.create(name=groupname)
    user.groups = [group]
    user_profile.group = group
    user_profile.save()
    EMAIL_SUBJECT = 'Phonelab Admin Authorization'

  elif user_profile.user_type=='M':
    group = Group.objects.get(name=groupname)
    user.groups = [group]
    user_profile.group = group
    user_profile.save()
    EMAIL_SUBJECT = 'Phonelab Leader Authorization'
    
  current_site = Site.objects.get_current()
  c = Context({'user': user, 'group': group ,'user_type': user_profile.user_type, 'key': activation_key, 'site_name': current_site})
  EMAIL_BODY = (loader.get_template('users/mails/user_signup.txt')).render(c)
  TO_EMAIL = [user.email]
  send_mail(EMAIL_SUBJECT, EMAIL_BODY, FROM_EMAIL, TO_EMAIL)

  return render_to_response(
          'users/confirm.html', 
          {'success': True,
           'user_type': user_profile.user_type,
           'req_user': user},
            context_instance=RequestContext(request)
         )


"""
Email activation 

@param: activation_key
@date 05/18/2010
@author TKI
"""

def confirm(request, activation_key):
  user_profile = get_object_or_404(UserProfile, activation_key=activation_key)
  user = user_profile.user

  if user.is_active:
    return render_to_response(
             'users/confirm.html', 
             {'has_account': True,
              'req_user': user},
             context_instance=RequestContext(request)
           )
  
  if user_profile.key_expires < datetime.datetime.today():
    return render_to_response(
             'users/confirm.html', 
             {'expired': True},
             context_instance=RequestContext(request)
           )

  if user_profile.user_type == 'M':
    user.is_active = True
    user.save()
    return render_to_response(
           'users/confirm.html',
           {'req_user': user,
           'activated': True,
           'user_type': user_profile.user_type},
           context_instance=RequestContext(request)
          )

  if user_profile.user_type == 'L':
    user.is_active = True
    user.save()
    return render_to_response(
           'users/confirm.html',
           {'req_user': user,
           'activated': True,
           'user_type': user_profile.user_type},
           context_instance=RequestContext(request)
          )


  
  return render_to_response(
           'users/confirm.html', 
           {'activated': True,
            'user_type': user_profile.user_type},
           context_instance=RequestContext(request)
           )
  
"""
User Profile

@date 05/21/2010
@author TKI
"""
@login_required
def profile(request, userId):
  group = {}
  leader = {}
  members = {}
  # define default response
  response = {"err": "", "data": ""}
  try:
    # get UserProfile with user foreignkey
    userprofile = UserProfile.objects.get(user=userId)

    if userprofile.user_type == 'P':
      # get DeviceProfile with devprofile foreignkey
      devprofiles = DeviceProfile.objects.filter(user=userId)

    if userprofile.user_type == 'A':
      #get all devices
      devprofiles = DeviceProfile.objects.all()

    #get group its leader and members and its devices
    if(userprofile.user_type== 'M' or userprofile.user_type=='L'):
      group = Group.objects.get(user = userId)
      devprofiles = DeviceProfile.objects.filter(group=group)
      leader = get_object_or_404(UserProfile, user_type='L', group=group) 
      members = UserProfile.objects.filter(user_type='M', group=group)
    return render_to_response(
             'users/profile.html', 
             { 'userprofile' : userprofile,
               'group': group,
               'leader': leader,
               'members': members, 
               'devprofiles'  : devprofiles },
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
Edit User Profile Form [GET]

@date 05/21/2012
@param String userId

@author TKI
"""
@login_required
def edit(request, userId):
  # define default response
  response = { "err": "", "data": "" }
  try:
    # get UserProfile with user foreignkey
    userprofile = UserProfile.objects.get(user=userId)    
    return render_to_response(
             'users/edit.html', 
             { 'userprofile' : userprofile},
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
    return HttpResponseRedirect('/accounts/profile/' + userId)
# User does not exist
  except Device.DoesNotExist: 
    response['err'] = {
      'no' : 'err1',
      'msg': 'invalid user'
    }
  return json_response_from(response)





