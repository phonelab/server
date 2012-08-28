from django.contrib import admin
from django.conf.urls.defaults import *
from users.models import UserProfile, Participant
from device.models import Device, DeviceApplication, DeviceProfile, DumpServices, StatusMonitor
from device.models import HeartbeatStatus, OtaStatus
from application.models import Application
from transaction.models import Transaction, TransactionDevApp
from experiment.models import Experiment, ExperimentProfile
from settings import FROM_EMAIL, ADMINS
from django.template import Context, loader
from django.contrib.auth.models import User
from django.core.mail import send_mail
from lib.helper import json_response_from, json
from datetime import datetime, timedelta
from django.contrib.admin import SimpleListFilter

#TODO: change location and implement inline
#Inline reference: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.InlineModelAdmin
"""
Admin site interface

@date 05/25/2012

@author Taeyeon
"""

class DeviceAdmin(admin.ModelAdmin):
  list_display = ('id', 'meid', 'hash_meid', 'reg_id')
  search_fields = ['meid']
admin.site.register(Device, DeviceAdmin)
#admin.site.register(Device)

class HeartbeatStatusAdmin(admin.ModelAdmin):
  list_display = ('dev_meid', 'status_value', 'build_version', 'latitude', 'longitude', 'timestamp')
  search_fields = ['dev__meid']
admin.site.register(HeartbeatStatus, HeartbeatStatusAdmin)

class OtaStatusAdmin(admin.ModelAdmin):
  list_display = ('dev_meid', 'status_value', 'timestamp')
  search_fields = ['dev__meid']
admin.site.register(OtaStatus, OtaStatusAdmin)

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

class DumpServicesAdmin(admin.ModelAdmin):
  list_display = ('id', 'parameter')
admin.site.register(DumpServices, DumpServicesAdmin)

class StatusMonitorAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'value', 'units')
admin.site.register(StatusMonitor, StatusMonitorAdmin)

#send email to participants
def send_email(modeladmin, request, queryset):
    for obj in queryset:
      EMAIL_SUBJECT = 'Email RequestContext'
      c = Context({'name': obj.name })
      EMAIL_BODY = (loader.get_template('users/mails/participant_device_approval.txt')).render(c)
      TO_EMAIL = [obj.email]
      send_mail(EMAIL_SUBJECT, EMAIL_BODY, FROM_EMAIL, TO_EMAIL)

    queryset.update(approved=1)

class ParticipantAdmin(admin.ModelAdmin):
  list_display = ('name', 'email', 'student_status', 'expected_grad', 'submitted_time', 'result')
  search_fields = ['email', 'name']
  list_filter = ['student_status', 'expected_grad']
  actions = [send_email]
  # list_display_links = ['send_email']
admin.site.register(Participant, ParticipantAdmin)

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

#admin experiment approval
def approve_experiment(modeladmin, request, queryset):
  for obj in queryset:
    # define default response
    response = { "err": "", "data": "" }
    # return if GET request
    if request.method == 'GET':
      response['err'] = {
        'no' : 'err0',
        'msg': 'sorry no gets'
      }
      return HttpResponseRedirect('/error/')

    dev_ids = obj.dev.all()
    app_ids = obj.app.all()
    transact = Transaction()
    transact.eid = obj
    transact.user = User.objects.get(id__in=obj.user.all)
    transact.total = len(dev_ids) * len(app_ids)
    transact.progress = 0

  #Check Data Validation
  for dev_id in dev_ids:
    for app_id in app_ids:
      #check FailureAlready(F1)
      if DeviceApplication.objects.filter(dev=dev_id).filter(app=app_id):
        response['err'] = {
          'no' : 'err1',
          'msg': 'The application is already installed'
        }
        return json_response_from(response)
  
  #insert the data from POST method
  for dev_id in dev_ids:
    for app_id in app_ids:
      transact.save()
      t_id = transact.id
      trndevapp = TransactionDevApp()
      trndevapp.tid = Transaction.objects.get(id=t_id)
      trndevapp.dev = dev_id
      trndevapp.app = app_id
      trndevapp.action = 'I'
      trndevapp.result = "N" # N is N/A
      trndevapp.save()
      Device.objects.filter(id=dev_id.id).update(active="D")

  msg = "new_manifest"
  for dev_id in dev_ids:
    Device.objects.get(id=dev_id.id).send_message(payload=json({"message": msg}))

  eprofile = ExperimentProfile.objects.get(experiment=obj)
  eprofile.starttime = datetime.now()
  print obj.period
  endtime = datetime.now() + timedelta(int(obj.period))
  print endtime
  eprofile.endtime = endtime
  eprofile.save()
  queryset.update(active=1)         

class ExperimentAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'description', 'tag', 'irb', 'active')
  actions = [approve_experiment]
  list_filter = ['active']
admin.site.register(Experiment, ExperimentAdmin)

class ExperimentProfileAdmin(admin.ModelAdmin):
  list_display = ('id', 'experiment')
admin.site.register(ExperimentProfile, ExperimentProfileAdmin)
