from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, Group
from django.shortcuts import render_to_response, get_object_or_404
from users.models import UserProfile
from experiment.models import Experiment, ExperimentProfile
from django.template import RequestContext
from application.models import Application
from device.models import DeviceProfile, Device
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

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
List all Experiments

@date 07/18/2012

@author Manoj
"""
@login_required
def index(request):

	user = request.user
	userprofile = UserProfile.objects.get(user=user)
	group = userprofile.group

	experiments = Experiment.objects.filter(group=group).order_by('id')

	return render_to_response(
			'experiment/exp_page.html',
			{
			 'user': user,
			 'userprofile': userprofile,
			 'group': group,
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
  	members = UserProfile.objects.filter(group=userprofile.group, user_type = 'M')
  	apps = Application.objects.filter(group=userprofile.group)
  	devices = DeviceProfile.objects.filter(group=userprofile.group)
  	# query the database for all applications
  	return render_to_response(
    	  	'experiment/new_exp_form.html', 
    	  	{
    	  	'group': userprofile.group,
        	'members': members,
        	'devices'  : devices,
        	'apps': apps,
       	 	'exp': exp,
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
	leader_profile = UserProfile.objects.get(user_type='L', group=experiment.group)
	leader = leader_profile.user
	members_to_add = UserProfile.objects.filter(group=experiment.group, user_type='M').exclude(user__in=experiment.user.all())
	devices_to_add = DeviceProfile.objects.filter(group=experiment.group).exclude(dev__in=experiment.dev.all())
	apps_to_add = Application.objects.filter(group=experiment.group).exclude(id__in=experiment.app.all())
	return render_to_response (
			'experiment/experiment_profile.html', 
  	  		{'user':user,
  	  		 'userprofile': userprofile,
  	  		 'group': experiment.group,
  	  		 'leader': leader,
  	  		 'members_to_add': members_to_add,
  	  		 'devices_to_add': devices_to_add,
  	  		 'apps_to_add': apps_to_add,
  	  		 'experiment': experiment },
      		context_instance=RequestContext(request)
    	  )

"""
Create new experiment

@date 07/18/2012

@author Manoj
"""

def create_experiment(request):
	user = request.user
	userprofile = UserProfile.objects.get(user=user)
	group = Group.objects.get(user=user)
	leader = UserProfile.objects.get(user_type='L', group=group) 

	if request.POST:
		exp = Experiment (
			group = group,
			name = request.POST['name'],
			description = request.POST['desc'],
			tag = request.POST['Tag']
			)
		exp.save()

		members = request.POST.getlist('members')
		devs = request.POST.getlist('devs')
		apps = request.POST.getlist('apps')

		for member in members:
			exp.user.add(User.objects.get(username=member))

		for dev in devs:
			exp.dev.add(dev)

		for app in apps:
			exp.app.add(app)

		exp.save()
		exp_profile = ExperimentProfile (eid=exp)
		exp_profile.save()

		return HttpResponseRedirect('/experiment/' + str(exp.id))

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
Delete a member

@date 07/18/2012

@param expId, member

@author Manoj
"""
@login_required
def delete_member(request, expId, member):

	userprofile = get_object_or_404(UserProfile, user=request.user)
	if userprofile.user_type == 'L':
		member = User.objects.get(username=member)
		experiment = Experiment.objects.get(id=expId)
		experiment.user.remove(member)

		return HttpResponseRedirect('/experiment/' + expId)

	else:

		return HttpResponseRedirect('/')


"""
Delete a Device

@date 07/18/2012

@param expId, deviceId

@author Manoj
"""
@login_required
def delete_device(request, expId, deviceId):

	userprofile = get_object_or_404(UserProfile, user=request.user)
	if userprofile.user_type == 'L':
		device = Device.objects.get(id=deviceId)
		experiment = Experiment.objects.get(id=expId)
		experiment.dev.remove(device)
	
		return HttpResponseRedirect('/experiment/' + expId)

	else:
		return HttpResponseRedirect('/')


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
