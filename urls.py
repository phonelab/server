from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

if settings.DEBUG:
  urlpatterns = patterns('',
    url(r'^manifest/(?P<deviceId>[A-Z0-9]\w+)/$', 'controller.views.download_manifest'),
    url(r'^log/(?P<deviceId>[A-Z0-9]\w+)/$', 'datalogger.views.upload_file'),

    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # url(r'^admin/', include(admin.site.urls)),
  )
