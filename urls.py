from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

if settings.DEBUG:
  urlpatterns = patterns('',
    #####
    ##### Web Endpoints
    ##### Used by Admin and others
    #####
    
    #
    ## Device
    #
    # All Devices [GET]
    url(r'^devices/$', 'device.views.index'),
    # Single Device [GET]
    url(r'^device/(?P<deviceId>[A-Z0-9]\w+)/$', 'device.views.show'),


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
