import re
from django import forms
from django.contrib.auth.models import User, Group
from users.models import UserProfile, Participant
from django.shortcuts import get_object_or_404
from django.forms.widgets import RadioSelect 
 
"""
RigistrationForm

@date 03/07/2012

@author Taeyeon
"""
class RegistrationForm(forms.Form):

  CHOICE = (
    (u'E',u'Experimenter'), 
    (u'P', u'Participant'),
  )

  username =forms.CharField(label=u'Username', max_length=30)
  email = forms.EmailField(label=u'Email')
  password1 = forms.CharField(
    label=u'Create a password',
    widget=forms.PasswordInput()
  )
  password2 = forms.CharField(
    label=u'Confirm your password',
    widget=forms.PasswordInput()
  )
  user_type = forms.ChoiceField(choices=CHOICE)
  def clean_username(self):
    username = self.cleaned_data['username']
    if not re.search(r'^\w+$', username):
      raise forms.ValidationError('Username can only Contain '
        'alphanumeric characters and the underscore.')
    try:
      User.objects.get(username=username)
    except User.DoesNotExist:
      return username
    raise forms.ValidationError('The username "%s" is already taken.' % username)
  
  def clean_password2(self):
    if 'password1' in self.cleaned_data:
      password1 = self.cleaned_data['password1']
      password2 = self.cleaned_data['password2']
      if password1 == password2:
        return password2
      else:
        raise forms.ValidationError('The two password fields did not match.')

  def save(self, new):
    u = User.objects.create_user(new.cleaned_data['username'], new.cleaned_data['email'], new.cleaned_data['password1'])
    u.is_active = False
    u.save()
    return u


"""
Particiapnt email list

@date 07/23/2012

@author Manoj
"""
STUDENT_CHOICES = (
  (u'F', u'Freshman'),
  (u'SO', u'Sophomore'),
  (u'J', u'Junior'),
  (u'SE', u'Senior'),
  (u'G', u'Graduate'),
  (u'P', u'PhD'),
  )
class ParticipantForm(forms.Form):
  name =forms.CharField(label=u'Full Name', max_length=50)
  email = forms.EmailField(label=u'Email')
  student_status = forms.ChoiceField(choices=STUDENT_CHOICES, label=u'During 2012-2013 you will be?')

  def clean_email(self):
    email = self.cleaned_data['email']
    try:
      Participant.objects.get(email=email)
    except Participant.DoesNotExist:
      return email
    raise forms.ValidationError('The email "%s" has already been registered. Thank You!' % email)

  
    



