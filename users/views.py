from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import send_mail
from django.template import RequestContext, Context, loader
from django.http import HttpResponseRedirect

from settings import FROM_EMAIL, ADMINS
from users.models import UserProfile
from users.forms import RegistrationForm
import datetime, random, sha
 
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
      user = form.save(form)
      # Save the user                                                                                                                                                 
#      user = form.save()
#      user.backend = 'django.contrib.auth.ackends.ModelBackend'
#      user.groups.add(Group.objects.get(name='Regular'))
#      login(request, user)
#      Profile.objects.create(user = user)
     
      # Build the activation key for their account                                                                                                                    
      salt = sha.new(str(random.random())).hexdigest()[:5]
      activation_key = sha.new(salt+user.username).hexdigest()
      key_expires = datetime.datetime.today() + datetime.timedelta(2)

      # Create and save their profile                                                                                                                                 
      new_profile = UserProfile(user=user, activation_key=activation_key, key_expires=key_expires)
      new_profile.save()

      # Send an email with the confirmation link                                                                                                                      
      EMAIL_SUBJECT = 'The signup information you requested'
      c = Context({'user': user.username, 'key': new_profile.activation_key})
      EMAIL_BODY = (loader.get_template('users/user_signed_up.txt')).render(c)

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

            
#      return render_to_response(
#               'users/register.html', 
#               {'created': True},
#               context_instance=RequestContext(request)
#             )
#    else:
#      errors = new_data = {}
#    form = forms.FormWrapper(form, new_data, errors)
#  return render_to_response(
#          'users/register.html', 
#           {'form': form},
#           context_instance=RequestContext(request)
#           )

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
def register(request):
  if request.method == 'POST':
    form = SignupForm(request.POST)
    if form.is_valid():
      user = User.objects.create_user(
        username=form.cleaned_data['username'],
        password=form.cleaned_data['password1'],
        email=form.cleaned_data['email']
      )
      return HttpResponseRedirect('/')
  else:
    form = RegistrationForm()
  return render_to_response(
           'users/register.html',
           { 'form': form },
           context_instance=RequestContext(request)
         )

"""
