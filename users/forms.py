from django import forms
from django.contrib.auth.models import User, Group
from users.models import UserProfile, Participant
from django.shortcuts import get_object_or_404
from django.forms.widgets import RadioSelect 
import string, re
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
  (u'X', u'During 2012-2013 you will be?'),
  (u'F', u'Freshman'),
  (u'SO', u'Sophomore'),
  (u'J', u'Junior'),
  (u'SE', u'Senior'),
  (u'G', u'Graduate'),
  (u'P', u'PhD'),
  (u'ST', u'Staff'),
  (u'FA', u'Faculty'),
  )
GRADUATION_MONTH_CHOICES = (
  (u'M', u'Month'),
  (u'02', u'February'),
  (u'06', u'June'),
  (u'09', u'September'),
  )
GRADUATION_YEAR_CHOICES = (
  (u'Y', u'Year'),
  (u'12', u'2012'),
  (u'13', u'2013'),
  (u'14', u'2014'),
  (u'15', u'2015'),
  (u'16', u'2016'),
  (u'17', u'2017'),
  (u'18', u'2018'),
  (u'19', u'2019'),
  (u'20', u'2020'),
  )
class ParticipantForm(forms.Form):
  is_not_student = 'enabled'
  name =forms.CharField(label=u'Full Name', max_length=50)
  email = forms.EmailField(label=u'Email', widget=forms.TextInput(attrs={'placeholder': 'example@buffalo.edu'}))
  student_status = forms.ChoiceField(choices=STUDENT_CHOICES, label=u'During 2012-2013 you will be?', widget=forms.Select(attrs={'onchange': 'return disable_graduation()'}))
  expected_grad_month = forms.ChoiceField(choices=GRADUATION_MONTH_CHOICES, required=False, widget=forms.Select(attrs={'class': 'input-small'} ))
  expected_grad_year = forms.ChoiceField(choices=GRADUATION_YEAR_CHOICES, required=False, label=u'Expected Graduation Date', widget=forms.Select(attrs={'class': 'input-small'}))
  
  def clean_email(self):
    email = self.cleaned_data['email']
    try:
      Participant.objects.get(email=email)
    except Participant.DoesNotExist:
      if(email.find('@buffalo.edu')>0):
        return email
      else: 
        raise forms.ValidationError('Please enter your UB Mail id')
    raise forms.ValidationError('The email "%s" has already been registered. Thank You!' % email)

  def clean_student_status(self):
    status = self.cleaned_data['student_status']
    if status == 'X':
      raise forms.ValidationError('Please Select your student status during the year 2012-2013')
    else:
      return status

  def clean_expected_grad_month(self):
    month = self.cleaned_data['expected_grad_month']
    status = self.cleaned_data['student_status']
    if not (status == 'FA' or status == 'ST'):
      if month == 'M':
        raise forms.ValidationError('Please Select the month your expected to Graduate')
      else:
        return month

  def clean_expected_grad_year(self):
    year = self.cleaned_data['expected_grad_year']
    status = self.cleaned_data['student_status']
    if not (status == 'FA' or status == 'ST'):
      if year == 'Y':
        raise forms.ValidationError('Please Select the Year your expected to Graduate')
      else:
        return year


  
"""
Particiapnt Register and Device Register

@date 08/13/2012

@author TKI
"""
class ParticipantRegisterForm(forms.Form):
  lib_number = forms.CharField(label=u'Library Number', max_length=14, widget=forms.TextInput(attrs={'onkeypress': 'return convert_tab(this, event)'}))
  meid = forms.CharField(label=u'MEID', max_length=15, widget=forms.TextInput(attrs={'onkeypress': 'return convert_tab(this, event)'}))
  phone_number = forms.CharField(label=u'Phone Number?', max_length=10, widget=forms.TextInput(attrs={'onkeypress': 'return convert_tab(this, event)'}))
  
  def clean_lib_number(self):
    lib_number = self.cleaned_data['lib_number']
    if lib_number.isdigit():
        return lib_number
    else: 
        raise forms.ValidationError('Please enter proper Library Number')
  
  def clean_meid(self):
    meid = self.cleaned_data['meid']
    if len(meid) ==  14:
      if (meid in string.hexdigits):
        raise forms.ValidationError('Please enter proper 4G MEID')
      else: 
        return meid
    elif len(meid) == 15: 
      if meid.isdigit():
        return meid
      else: 
        raise forms.ValidationError('Please enter proper 3G IMEI')
    else:
        raise forms.ValidationError('Please enter proper MEID')

  def clean_phone_number(self):
    phone_number = self.cleaned_data['phone_number']
    if phone_number.isdigit():
        return phone_number
    else: 
        raise forms.ValidationError('Please enter proper Phone Number')
