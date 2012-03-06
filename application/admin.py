from django.contrib import admin
from server.application.models import Application

class ApplicationAdmin(admin.ModelAdmin):
  pass
admin.site.register(Application, ApplicationAdmin)
