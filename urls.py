from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

#admin interface
from django.contrib import admin
admin.autodiscover()

if settings.DEBUG:
  urlpatterns = patterns('',
    #####
    ##### Web Endpoints
    ##### Used by Admin and others
    #####
    #main_page
    url(r'^$', 'device.views.main_page'),
    #Admin interface for django version 1.3
    url(r'^admin/', include(admin.site.urls)),
    #login page
    url(r'^login/$', 'django.contrib.auth.views.login'),


    #
    ## Device
    #
    # All Devices [GET]
    url(r'^devices/$', 'device.views.index'),
    # Single Device [GET]
    url(r'^device/(?P<deviceId>[A-Z0-9]\w+)/$', 'device.views.show'),
    # Edit Device Form [GET]
    url(r'^device/(?P<deviceId>[A-Z0-9]\w+)/edit/$', 'device.views.edit'),
    # Update Device Form [GET]
    url(r'^device/(?P<deviceId>[A-Z0-9]\w+)/update/$', 'device.views.update'),
	# REFACTOR: C2DM [GET]
    url(r'^device/(?P<deviceId>[A-Z0-9]\w+)/c2dm/$', 'device.views.c2dm'),
    # Log Tag filter[GET]
    url(r'^device/(?P<deviceId>[A-Z0-9]\w+)/tag/$', 'datalogger.views.show_tag'),
    # TODO: Phone Status [GET]
    url(r'^device/(?P<deviceId>[A-Z0-9]\w+)/status/(?P<statusType>\d{1})/$', 'device.views.status'),
	  # Log Data [GET]
    url(r'^device/(?P<deviceId>[A-Z0-9]\w+)/(?P<logFilename>[0-9]\w+).log$', 'datalogger.views.show'),
	  # Update Status
    # url(r'^device/(?P<deviceId>[A-Z0-9]\w+)/update/status/$', 'device.views.update_status'),
    
    #####
    ##### API Endpoints
    ##### Used by PhoneLab Application on Device
    #####

    #
    ## Device
    #
    # New device registration [POST]
    # Update Previous device registration [POST]
    url(r'^device/$', 'device.views.create_or_update_device'),
    # Device Status [POST]
    #url(r'^devicestatus/(?P<deviceId>[A-Z0-9]\w+)/$', 'device.views.device_status'),

    #
    ## Manifest
    #
    # Download Manifest [GET]
    url(r'^manifest/(?P<deviceId>[A-Z0-9]\w+)/$', 'manifest.views.download_manifest'),

    #
    ## Logger
    #
    # POST Logfiles [POST]
    url(r'^log/(?P<deviceId>[A-Z0-9]\w+)/$', 'datalogger.views.upload_log'),

    #
    ## Application
    #
    # Download Application [GET]
    url(r'^experiment/(?P<appId>[0-9]\w+).apk$', 'application.views.get_download'),

    #
    ## Error
    ## TODO
    # Error Handling [POST]
    # url(r'^error/(?P<deviceId>[A-Z0-9]\w+)/$', 'error.views.create_error'),
  )
