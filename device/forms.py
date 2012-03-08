import re
from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
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
  def clean_username(self):
    username = self.cleaned_data['username']
    if not re.search(r'^\w+$', username):
      raise forms.ValidationError('Username can only Contain '
        'alphanumeric characters and the underscore.')
    try:
      User.objects.get(username=username)
    except User.DoesNotExist:
      return username
    raise forms.ValidationError('Username is already taken.')
  
  def clean_password2(self):
    if 'password1' in self.cleaned_data:
      password1 = self.cleaned_data['password1']
      password2 = self.cleaned_data['password2']
      if password1 == password2:
        return password2
    raise forms.ValidationError('passwords do not match')


