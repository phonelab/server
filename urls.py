from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

if settings.DEBUG:
  urlpatterns = patterns('',
    #
    ## Device
    #
    # New device registration [POST]
    url(r'^device/$', 'device.views.create'),
    # Device List [GET]
    url(r'^devices/$', 'device.views.index'),
    # Device Show [GET]
    url(r'^device/(?P<deviceId>[A-Z0-9]\w+)$', 'device.views.show'),

    #
    ## Controller
    #
    # Manifest [GET]
    url(r'^manifest/(?P<deviceId>[A-Z0-9]\w+)/$', 'controller.views.download_manifest'),

    #
    ## Logger
    #
    # Logger [POST]
    url(r'^log/(?P<deviceId>[A-Z0-9]\w+)/$', 'datalogger.views.upload_file'),
  )
