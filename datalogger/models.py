from django.db import models
from django import forms

class UploadFileForm(forms.Form):
  title = forms.CharField(max_length=50)
  file = forms.FileField()
