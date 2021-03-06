from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, Group
from django.shortcuts import render_to_response, get_object_or_404
from users.models import UserProfile
from experiment.models import Experiment, ExperimentProfile
from django.template import RequestContext, Context, loader
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from settings import FROM_EMAIL, ADMINS
from application.models import Application
from device.models import DeviceProfile, Device
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
import os, errno, mimetypes
from django.conf import settings
from django.core.servers.basehttp import FileWrapper
from django.utils.encoding import smart_str
RAW_APP_ROOT = settings.RAW_APP_ROOT
RAW_IRB_ROOT = settings.RAW_IRB_ROOT

admin_mail = 'tempphonelab@gmail.com'

# usage: @user_passes_test(is_leader, login_url='/login')
# usage: @user_passes_test(is_member, login_url='/login')
def is_member(user):
  if user:
    return UserProfile.objects.filter(user=user).filter(user_type=M) > 0
  return False

def is_leader(user):
  if user:
    return UserProfile.objects.filter(user=user).filter(user_type=L) > 0
  return False


"""
Download IRB Letter

@date 08/06/2012

@param irbId

@author Manoj
"""
@login_required
def download_irb(request, irbId):
	# define default response
  response = { "err": "", "data": "" }
  # return if GET request
  if request.method == 'POST':
    response['err'] = {
      'no' : 'err0',
      'msg': 'sorry no POST'
    }
    return HttpResponseRedirect('/error/')
  # Get irb
  # irb = Experiment.objects.filter(irb=irbId)
  # if application exists, render download
  path = os.path.join(RAW_IRB_ROOT, str(irbId)+'.pdf')
  wrapper = FileWrapper(open(path, "r"))
  content_type = mimetypes.guess_type(path)[0]
  response = HttpResponse(wrapper, content_type = content_type) 
  response['Content-Length'] = os.path.getsize(path)
  response['Content-Disposition'] = 'attachment; filename=%s' %smart_str(os.path.basename(path))
  return response
  

"""
List all Experiments

@date 07/18/2012

@author Manoj
"""
@login_required
def index(request):

	user = request.user
	userprofile = UserProfile.objects.get(user=user)
	
	experiments = Experiment.objects.filter(user=user).order_by('id')

	return render_to_response(
			'experiment/exp_page.html',
			{
			 'userprofile': userprofile,
			 'experiments':experiments
			},
			context_instance=RequestContext(request)
		  )


"""
Upload experiment form

@date 07/18/2012

@author Manoj
"""
@login_required
def new(request):

	exp = Experiment()
	user = request.user
	userprofile = UserProfile.objects.get(user=user)
  	# query the database for all applications
  	return render_to_response(
    	  	'experiment/new_exp_form.html', 
    	  	{
       	 	'userprofile': userprofile
      	  	},
      		context_instance=RequestContext(request)
    	  )

"""
Show single experiment

@date 07/18/2012

@param expId

@author Manoj
"""
@login_required
def show(request, expId):
	
	user = request.user
	userprofile = UserProfile.objects.get(user=user)
	experiment = Experiment.objects.get(id = expId)
	
	return render_to_response (
			'experiment/experiment_profile.html', 
  	  		{
  	  		 'userprofile': userprofile,
  	  		 'experiment': experiment },
      		context_instance=RequestContext(request)
    	  )

"""
Create new experiment

@date 07/18/2012

@author Manoj
"""

def create_experiment(request):

	# define default response
	response = { "err": "", "data": "" }

	#initialize a counter for apps
	i = 0
	j = 0

	#initialize filename
	filenames = {}
	filedirs = {}

	if request.POST:

		period = request.POST['duration']
		unit = request.POST['dur_unit']
		
		if unit == 'W':
			period = int(period)*7
		elif unit == 'M':
			period = int(period)*30

		# Save Experiment
		exp = Experiment (
			name = request.POST['expname'],
			description = request.POST['expdesc'],
			tag = request.POST['exptag'],
			period = period,
			)
		exp.save()

		#upload IRB Letter
		file_type = request.FILES['irbletter'].content_type.split('/')[1]
		
		#save IRB Letter
		irbname = os.path.join(RAW_IRB_ROOT, str(exp.irb)+'.'+file_type)
		irbdir = os.path.dirname(irbname)

		try:
			os.mkdir(irbdir)
		except OSError, e:
			if e.errno != errno.EEXIST:
			  response['err'] = {
			    'no' : 'err1', 
			    'msg': 'cannot create dir, failed upload'
			  }
			  raise

		# get file handle
		fileHandle = open(irbname, 'wb+')
		for chunk in request.FILES['irbletter'].chunks():	
			# write it out
			fileHandle.write(chunk)
		# close file handle
		fileHandle.close()

		response['data'] = "done"

		#add user to the experiment
		exp.user.add(request.user)
		
		devs = Device.objects.all()
		appnames = request.POST.getlist('appname')
		appdescs = request.POST.getlist('appdesc')
		apptypes = request.POST.getlist('apptype')
		
		#add the devices to the experiment
		for dev in devs:	
			exp.dev.add(dev)

		#add the apps to the experiment
		for app in appnames:
			
			application = Application(
	        				user = request.user,
	        				name = app,
					        #package_name = params['package_name'],
					        #intent_name  = params['intent_name'],
					        description   = appdescs[i],
					        type          = apptypes[i],
					        active        = "E"
					      )
					        
					        #version      = params["version"],
			application.save()
			exp.app.add(application)
			i = i+1

			#create dirs for Applications
			filename = os.path.join(RAW_APP_ROOT, str(application.id) + ".apk")
			filedir = os.path.dirname(filename)
			filenames[app] = filename
			filedirs[app] = filedir

		exp.save()

		exp_profile = ExperimentProfile (experiment=exp)
		exp_profile.starttime = datetime.now()
		exp_profile.endtime = datetime.now()
		exp_profile.save()

		#upload experiment
		for afile in request.FILES.getlist('upload'):
			# create folder for user if it doesn`t exist
			try:
				os.mkdir(filedirs[appnames[j]])
			except OSError, e:
				if e.errno != errno.EEXIST:
				  response['err'] = {
				    'no' : 'err1', 
				    'msg': 'cannot create dir, failed upload'
				  }
				  raise

			# get file handle
			fileHandle = open(filenames[appnames[j]], 'wb+')
			# write it out
			for chunk in afile.chunks():
				fileHandle.write(chunk)
			# close file handle
			fileHandle.close()
			j = j+1
			response['data'] = "done"
		
		#Notify the admin about the new experiment for approval
   		current_site = Site.objects.get_current()
	 	EMAIL_SUBJECT = 'Phonelab Experiment Authorization'
	 	c = Context({'user': request.user, 'exp': exp, 'site_name': current_site})
	  	EMAIL_BODY = (loader.get_template('experiment/mails/exp_authorization_request.txt')).render(c)
	  	TO_EMAIL = [admin_mail]
	  	send_mail(EMAIL_SUBJECT, EMAIL_BODY, FROM_EMAIL, TO_EMAIL)

	else:
		response["err"] = "err1"


	return HttpResponseRedirect('/experiments/')


"""
Update Experiment Profile

@date 07/18/2012

@param expId

@author Manoj
"""
def update(request, expId):

	params = request.POST
	# get UserProfile with user foreignkey
	user = request.user
	userprofile = UserProfile.objects.get(user=user)    
	experiment = Experiment.objects.get(id=expId)

	# Experiment Name
	if ('name' in params and experiment.name != params['name']):
		experiment.name = params['name']
	#Members
	if ('members' in params):
		for member in request.POST.getlist('members'):
			experiment.user.add(User.objects.get(username=member))
	# Devices
	if ('devs' in params):
		for dev in request.POST.getlist('devs'):
			experiment.dev.add(dev)
	#Applications
	if ('apps' in params):
		for app in request.POST.getlist('apps'):
			experiment.app.add(app)
	# save experiment profile
	experiment.save()
	# redirect to /accounts/profile/userId
	return HttpResponseRedirect('/experiment/' + expId)


"""
Delete Experiment

@date 07/18/2012

@param expId

@author Manoj
"""
@login_required
def delete_exp(request, expId):
	userprofile = get_object_or_404(UserProfile, user=request.user)
	if userprofile.user_type == 'L':

		experiment = Experiment.objects.get(id=expId)
		experiment.delete()

		return HttpResponseRedirect('/experiments/')

	else:
		return HttpResponseRedirect('/')


"""
Add a member

@date 07/18/2012

@param expId, member

@author Manoj
"""
@login_required
def add_member(request, expId):

	userprofile = get_object_or_404(UserProfile, user=request.user)
	experiment = Experiment.objects.get(id = expId)
	membername = request.POST['member']
	try:
		member = User.objects.get(username=membername)
	
	except User.DoesNotExist: 
		return render_to_response ('experiment/experiment_profile.html', 
  	  		 {'userprofile': userprofile,
  	  		 'no_member': True,
  	  		 'experiment': experiment },
      		context_instance=RequestContext(request)
    	  )

	current_site = Site.objects.get_current()
	EMAIL_SUBJECT = 'Invitation to join Phonelab Experiment'
  	c = Context({'user': request.user, 'experiment': experiment, 'member': member, 'site_name': current_site})
  	EMAIL_BODY = (loader.get_template('experiment/mails/experiment_invite.txt')).render(c)
  	TO_EMAIL = [member.email]
  	send_mail(EMAIL_SUBJECT, EMAIL_BODY, FROM_EMAIL, TO_EMAIL)

	return render_to_response ('experiment/experiment_profile.html', 
  	  		 {'userprofile': userprofile,
  	  		 'success': True,
  	  		 'experiment': experiment },
      		context_instance=RequestContext(request)
    	  )


"""
Delete a Device

@date 07/18/2012

@param expId, deviceId

@author Manoj
"""
@login_required
def join_member	(request, expId, userId):

	user = User.objects.get(id=userId)
	experiment = Experiment.objects.get(id=expId)
	experiment.user.add(user)
	experiment.save()
	
	return HttpResponseRedirect('/experiment/' + expId)


"""
Delete an Application

@date 07/18/2012

@param expId, appId

@author Manoj
"""
@login_required
def delete_app(request, expId, appId):

	userprofile = get_object_or_404(UserProfile, user=request.user)
	if userprofile.user_type == 'L':
		app = Application.objects.get(id=appId)
		experiment = Experiment.objects.get(id=expId)
		experiment.app.remove(app)
	
		return HttpResponseRedirect('/experiment/' + expId)

	else:
		return HttpResponseRedirect('/')
