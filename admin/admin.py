from django.contrib import admin
from django.conf.urls.defaults import *
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
  list_display = ('id', 'meid', 'reg_id')
  search_fields = ['meid']
admin.site.register(Device, DeviceAdmin)
#admin.site.register(Device)

class ApplicationAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'package_name', 'type')
  search_fields = ['name']
admin.site.register(Application, ApplicationAdmin)

#Todo: add function to change object name
class DeviceApplicationAdmin(admin.ModelAdmin):
  list_display = ('id', 'dev', 'app')
  search_fields = ['dev__meid']
admin.site.register(DeviceApplication, DeviceApplicationAdmin)


class TransactionAdmin(admin.ModelAdmin):
  list_display = ('id', 'user', 'total', 'progress')
admin.site.register(Transaction, TransactionAdmin)

class TransactionDevAppAdmin(admin.ModelAdmin):
  list_display = ('id', 'tid', 'dev', 'app', 'action', 'result')
admin.site.register(TransactionDevApp, TransactionDevAppAdmin)

class UserProfileAdmin(admin.ModelAdmin):
  list_display = ('user', 'user_type', 'activation_key', 'key_expires')
  search_fields = ['^user__username', '=user_type']
admin.site.register(UserProfile, UserProfileAdmin)

"""
Show status monitor for admin

@date 07/10/2012

@author TKI
"""
class StatusAdmin(admin.ModelAdmin):
  list_display = ('dev_meid', 'user', 'phone_no', 'status', 'last_log', 'plan', 'image_version', 'purpose', 'service_type')
  search_fields = ['dev__meid', '^user__username', 'phone_no']
  
#  def get_urls(self):
#    urls = super(StatusAdmin, self).get_urls()
#    my_urls = patterns('',
#      (r'^device/deviceprofile/$', self.admin_site.admin_view(self.status_monitor, cacheable=True))
#    )
#    return my_urls + urls
  
#  def status_monitor(self, request):
#    total = DeviceProfile.objects.count()
#    type_a = DeviceProfile.objects.filter(service_type="3").count()
#    type_b = total - type_a
#    no_working = DeviceProfile.objects.filter(status="W").count()
#    no_available = DeviceProfile.objects.filter(status="N").count()
#    return render_to_response(
#        'admin/admin/status_monitor.html', 
#        {
#        'total': total,
#        'user_type': userprofile.user_type
#      },
#        context_instance=RequestContext(request)
#    )
admin.site.register(DeviceProfile, StatusAdmin)

class ExperimentAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'description', 'tag')
admin.site.register(Experiment, ExperimentAdmin)

class ExperimentProfileAdmin(admin.ModelAdmin):
  list_display = ('id', 'experiment')
admin.site.register(ExperimentProfile, ExperimentProfileAdmin)
