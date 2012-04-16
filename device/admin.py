from django.contrib import admin
from device.models import Device, DeviceApplication
from application.models import Application
from transaction.models import Transaction, TransactionDevApp

class DeviceAdmin(admin.ModelAdmin):
#  pass	
  list_display = ('id', 'email', 'reg_id')
  search_fields = ['id', 'email']
admin.site.register(Device, DeviceAdmin)
#admin.site.register(Device)

class ApplicationAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'package_name')
#  pass
admin.site.register(Application, ApplicationAdmin)

#Todo: add function to change object name
class DeviceApplicationAdmin(admin.ModelAdmin):
  list_display = ('id', 'dev', 'app')
#  pass
admin.site.register(DeviceApplication, DeviceApplicationAdmin)


class TransactionAdmin(admin.ModelAdmin):
  list_display = ('id', 'user', 'total', 'progress')
#  pass
admin.site.register(Transaction, TransactionAdmin)

class TransactionDevAppAdmin(admin.ModelAdmin):
  list_display = ('id', 'dev', 'app', 'action', 'result')
#  pass
admin.site.register(TransactionDevApp, TransactionDevAppAdmin)
