from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import send_mail
from django.template import RequestContext, Context, loader
from django.http import HttpResponseRedirect
from django.contrib.sites.models import Site

from settings import FROM_EMAIL, ADMINS
#from django.utils import  simplejson as json
#from lib.helper import json_response_from, json
from django.contrib.auth.models import User
from users.models import UserProfile
from device.models import Device, DeviceProfile
from users.forms import RegistrationForm
import datetime, random, hashlib

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
#      user.groups.add(Group.objects.get(name='Regular'))
     
      # Build the activation key for their account                                                                                                                    
      salt = hashlib.md5(str(random.random())).hexdigest()[:5]
      activation_key = hashlib.md5(salt+user.username).hexdigest()
      key_expires = datetime.datetime.today() + datetime.timedelta(2)

      # Create and save their profile                                                                                                                                 
      new_profile = UserProfile(user=user, activation_key=activation_key, key_expires=key_expires)
      new_profile.save()
      # Send an email with the confirmation link                                                                                                                      
      EMAIL_SUBJECT = 'The signup information you requested'
      #TODO: remove the following two lines
      current_site = Site.objects.get_current()
      c = Context({'user': user.username, 'key': new_profile.activation_key, 'site_name': current_site.domain})
#      c = Context({'user': user.username, 'key': new_profile.activation_key})
      EMAIL_BODY = (loader.get_template('users/mails/user_signup.txt')).render(c)

      send_mail(EMAIL_SUBJECT, EMAIL_BODY, FROM_EMAIL, [user.email])

     # messages.success(request, u'Welcome to the PhoneLab Web Site!')
      return render_to_response(
               'users/register.html',
               { 'created': True,
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
  user_profile = get_object_or_404(UserProfile, activation_key=activation_key)
  if user_profile.key_expires < datetime.datetime.today():
    return render_to_response(
             'users/confirm.html', 
             {'expired': True},
             context_instance=RequestContext(request)
           )
  user_account = user_profile.user
  user_account.is_active = True
  user_account.save()
  return render_to_response(
           'users/confirm.html', 
           {'success': True},
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

    return render_to_response(
             'users/profile.html', 
             { 'userprofile' : userprofile,
               'devprofiles'  : devprofiles },
             context_instance=RequestContext(request)
             )
  # User does not exist
  except Device.DoesNotExist: 
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
  except Device.DoesNotExist: 
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
    # update
#    if ('update_interval' in params and device.update_interval != params['update_interval']):
#      device.update_interval = params['update_interval']
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





