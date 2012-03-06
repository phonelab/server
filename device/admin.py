from django.contrib import admin
from server.device.models import Device, DeviceApplication

class DeviceAdmin(admin.ModelAdmin):
#  pass	
  list_display = ('id', 'email', 'reg_id')
admin.site.register(Device, DeviceAdmin)
#admin.site.register(Device)

class DeviceApplicationAdmin(admin.ModelAdmin):
  pass
admin.site.register(DeviceApplication, DeviceApplicationAdmin)

#class ApplicationAdmin(admin.ModelAdmin):
#  pass
#admin.site.register(Application, ApplicationAdmin)
