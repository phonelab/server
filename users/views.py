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
from users.forms import RegistrationForm, Member_Group_Form
import datetime, random, hashlib
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist

site_name = '127.0.0.1:8000'
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
      # Save the user                                                                                                                                                 
      user = form.save(form)

      # Find the user type
      user_type = form.cleaned_data['user_type']
      # Build the activation key for their account                                                                                                                    
      salt = hashlib.md5(str(random.random())).hexdigest()[:5]
      activation_key = hashlib.md5(salt+user.username).hexdigest()
      key_expires = datetime.datetime.today() + datetime.timedelta(2)

     
      new_profile = UserProfile(user=user, activation_key=activation_key, key_expires=key_expires, user_type = user_type)
      current_site = Site.objects.get_current()
        
      if(user_type=='leader'):
        EMAIL_SUBJECT = 'Signup Authorization for an experiment Leader'
        
        c = Context({'user': user.username, 'email':user.email, 'key': new_profile.activation_key, 'site_name': site_name})
#       
        EMAIL_BODY = (loader.get_template('users/mails/leader_request.txt')).render(c)

        TO_EMAIL = ['manojmyl@buffalo.edu']

      elif(user_type=='member'):
        

        # Experiment leader name
        leader_name = request.POST['leader_name']
        # Define default response
        response = { "err": "", "data": "" }
        try:
          # get UserProfile with user foreignkey
          userId = User.objects.get(username=leader_name)
          leaderprofile = UserProfile.objects.get(user=userId)
          # Verify leader
          if(leaderprofile.user_type=='leader'):
            EMAIL_SUBJECT = 'Authorization for a Member to join your experiment group'
            c = Context({'user': user.username, 'email':user.email, 'leader_name':leader_name, 'key': new_profile.activation_key, 'site_name': site_name})
            EMAIL_BODY = (loader.get_template('users/mails/member_request.txt')).render(c)
            TO_EMAIL = [userId.email]

          else:
            
            return render_to_response(
                    'users/register.html',
                    {'not_leader': True,
                     'leader_name': leader_name},
                    context_instance=RequestContext(request)
                   )
        # User does not exist
        except User.DoesNotExist:
         
          return render_to_response(
                  'users/register.html',
                  {'no_such_user': True,
                   'leader_name': leader_name},
                   context_instance=RequestContext(request)
                 )
      
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
User group Creation/addition

@date 07/05/2012

@author Manoj
"""
def user_group_creation_or_addition(request, userId):
  
  userprofile = UserProfile.objects.get(user_id = userId)
  user = userprofile.user

  if userprofile.user_type == 'member':
    form = Member_Group_Form(request.POST)

    if form.is_valid():

      leader = form.check_leader(form)
      group = form.save(user, leader)
      user.is_active = True
      user.save()
      return render_to_response(
              'users/confirm.html',
              {'req_user': user,
               'activated': True,
               'user_type': userprofile.user_type},
              context_instance=RequestContext(request)
            )

    else:
      form = Member_Group_Form()

  return render_to_response(
          'users/confirm.html',
          {'req_user':user},
          context_instance=RequestContext(request)
        )


"""
Email Authorization

@date 07/03/2012

@author Manoj
"""

def authorize(request, activation_key):
  user_profile = get_object_or_404(UserProfile, activation_key=activation_key)
  user = user_profile.user

  c = Context({'user': user.username, 'user_type': user_profile.user_type, 'key': activation_key, 'site_name': site_name})
  EMAIL_BODY = (loader.get_template('users/mails/user_signup.txt')).render(c)
  TO_EMAIL = [user.email]

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

  
  elif user_profile.user_type == 'leader':
    EMAIL_SUBJECT = 'Phonelab Admin Authorization'
    

  elif user_profile.user_type=='member':
    EMAIL_SUBJECT = 'Phonelab Leader Authorization'
    
  

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

  if user_profile.user_type == 'member':
    return render_to_response(
<<<<<<< HEAD
          'users/group_addition.html',
=======
          'users/user_group.html',
>>>>>>> upstream/master
          {'user': user,
          'user_type': user_profile.user_type},
          context_instance=RequestContext(request)
          )

  user_account.is_active = True
  user_account.save()
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

  # define default response
  response = {"err": "", "data": ""}
  try:
    # get UserProfile with user foreignkey
    userprofile = UserProfile.objects.get(user=userId)    
    # get DeviceProfile with devprofile foreignkey
    devprofiles = DeviceProfile.objects.filter(user=userId)

    user = User.objects.get(id = userId)
    groups = Group.objects.filter(user = userId)
    return render_to_response(
             'users/profile.html', 
             { 'userprofile' : userprofile,
               'groups': groups,
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
    # ub_id
    if ('ub_id' in params and userprofile.ub_id != params['ub_id']):
      userprofile.ub_id = params['ub_id']
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





