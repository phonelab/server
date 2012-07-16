from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import login, logout, password_change

#admin interface
from django.contrib import admin
admin.autodiscover()


PASSWORD_CHANGE_DICT = {
                       'template_name': 'users/password_change.html',
                       'post_change_redirect': '/accounts/password_change/done/'
#                       'post_change_redirect': '/accounts/settings/'
}
PASSWORD_RESET_DICT = {
                      'post_reset_redirect': '/accounts/password_reset/done/',
                      'email_template_name': 'users/mails/password_reset.html',
                      'template_name': 'users/password_reset.html'
}

PASSWORD_RESET_CONFIRM_DICT = {
                              'post_reset_redirect': '/accounts/password_reset/complete/',
                              'template_name': 'users/password_reset_confirm.html',
}

if settings.DEBUG:
  urlpatterns = patterns('',
    #####
    ##### Web Endpoints
    ##### Used by Admin and others
    #####
    #main_page
    url(r'^$', 'device.views.main_page'),
    #Status Monitor for admin
    #url(r'^admin/statusmonitor/$', 'admin.views.status_monitor'),
    #Admin interface for django version 1.3
    url(r'^admin/', include(admin.site.urls)),
    #login page
    url(r'^login/$', login, {'template_name': 'users/login.html'}, name='login'),
    #logout page
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    #signup page
    url(r'^register/$', 'users.views.register'),
    #profile page
    url(r'^accounts/profile/(?P<userId>\d+)/$', 'users.views.profile'),
    # Edit User Profile Form [GET]
    url(r'^accounts/(?P<userId>\d+)/edit/$', 'users.views.edit'),
    # Update User Profile Form [POST]
    url(r'^accounts/(?P<userId>\d+)/update/$', 'users.views.update'),
    #signup authorization page
    url(r'^accounts/authorize/(?P<groupname>\w+)/(?P<activation_key>[a-z0-9]\w+)/$', 'users.views.authorize'),
    #signup confirm page
    url(r'^accounts/confirm/(?P<activation_key>[a-z0-9]\w+)/$', 'users.views.confirm'),
    #change password
    url(r'^accounts/password_change/$', password_change, PASSWORD_CHANGE_DICT, name='password_change'),
    #change password
    url(r'^accounts/password_change/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'users/password_change_done.html'}),
    #Password Reset
    url(r'^accounts/password_reset/$', 'django.contrib.auth.views.password_reset', PASSWORD_RESET_DICT),
    #Password Reset Done
    url(r'^accounts/password_reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'users/password_reset_done.html'}),
    #Password Reset Confirm
    url(r'^accounts/password_reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', PASSWORD_RESET_CONFIRM_DICT),
    #Password Reset Complete
    url(r'^accounts/password_reset/complete/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'users/password_reset_complete.html'}),


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
    # Phone Status [GET]
    url(r'^device/(?P<deviceId>[A-Z0-9]\w+)/status/(?P<statusType>\d{1})/$', 'device.views.status'),
	# Log Data [GET]
    url(r'^device/(?P<deviceId>[A-Z0-9]\w+)/(?P<logFilename>[0-9]\w+).log$', 'datalogger.views.show'),
	# Update Status
    # url(r'^device/(?P<deviceId>[A-Z0-9]\w+)/update/status/$', 'device.views.update_status'),

    #
    ## Application
    #
    # All Applications [GET]
    url(r'^experiments/$', 'application.views.index'),
    # Single Application [GET]
    url(r'^experiment/(?P<appId>\d+)/$', 'application.views.show'),
    # New Application Form [GET]
    url(r'^experiment/new/$', 'application.views.new'),
    # Withdraw Application
    url(r'^experiment/withdraw/(?P<appId>\d+)/$', 'application.views.withdraw'),
    # Edit Application Form [GET]
    #url(r'^experiment/(?P<appId>[A-Z0-9]\w+)/edit/$', 'application.views.edit'),
    # Create/Update Application [POST]
    url(r'^experiment/$', 'application.views.create_or_update_application'),

    
    #
    ## Transaction
    #
    # Get Transaction info [GET]
    url(r'^transactions/$', 'transaction.views.index'),
    # Transaction create [POST]
    # TransactionDevapp create
    url(r'^transaction/create/$', 'transaction.views.create'),
    # Get Transaction view [GET]
    url(r'^transaction/(?P<Id>\w+)/(?P<Type>\d)/$', 'transaction.views.show'),



    #####
    ##### API Endpoints
    ##### Used by PhoneLab Application on Device
    #####

    #
    ## Device
    
    #
    # New device registration [POST]
    # Update Previous device registration [POST]
    # Accepts: {}
    # Response : {}
    url(r'^device/$', 'device.views.create_or_update_device'),
    
    # Insert transaction related [POST]
    # Update transaction related [POST]
    # Accepts: {}
    # Response : {}
    url(r'^deviceapplication/$', 'device.views.insert_or_update_deviceapplication'),
    
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
    url(r'^experiment/(?P<appId>\d+).apk/$', 'application.views.get_download'),

    #
    ## Error
    ## TODO
    # Error Handling [POST]
    # url(r'^error/(?P<deviceId>[A-Z0-9]\w+)/$', 'error.views.create_error'),
  )
