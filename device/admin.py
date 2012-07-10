from django.contrib import admin
from users.models import UserProfile
from device.models import Device, DeviceApplication, DeviceProfile
from application.models import Application
from transaction.models import Transaction, TransactionDevApp
from experiment.models import Experiment, ExperimentProfile

#TODO: change location and implement inline
#Inline reference: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.InlineModelAdmin
"""
Admin site interface

@date 05/25/2012

@author Taeyeon
"""

class DeviceAdmin(admin.ModelAdmin):
  list_display = ('id', 'reg_id')
  search_fields = ['id']
admin.site.register(Device, DeviceAdmin)
#admin.site.register(Device)

class ApplicationAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'package_name')
admin.site.register(Application, ApplicationAdmin)

#Todo: add function to change object name
class DeviceApplicationAdmin(admin.ModelAdmin):
  list_display = ('id', 'dev', 'app')
admin.site.register(DeviceApplication, DeviceApplicationAdmin)


class TransactionAdmin(admin.ModelAdmin):
  list_display = ('id', 'user', 'total', 'progress')
admin.site.register(Transaction, TransactionAdmin)

class TransactionDevAppAdmin(admin.ModelAdmin):
  list_display = ('id', 'tid', 'dev', 'app', 'action', 'result')
admin.site.register(TransactionDevApp, TransactionDevAppAdmin)

class UserProfileAdmin(admin.ModelAdmin):
  list_display = ('user', 'user_type', 'activation_key', 'key_expires')
admin.site.register(UserProfile, UserProfileAdmin)

class DeviceProfileAdmin(admin.ModelAdmin):
  list_display = ('dev', 'user', 'phone_no', 'status', 'plan', 'image_version', 'purpose', 'service_type')
admin.site.register(DeviceProfile, DeviceProfileAdmin)

class ExperimentAdmin(admin.ModelAdmin):
  list_display = ('id', 'group', 'name', 'description', 'tag')
  #list_display = ('id', 'group', 'user', 'dev', 'app', 'name', 'description', 'tag')
admin.site.register(Experiment, ExperimentAdmin)

class ExperimentProfileAdmin(admin.ModelAdmin):
  list_display = ('id', 'eid')
admin.site.register(ExperimentProfile, ExperimentProfileAdmin)
