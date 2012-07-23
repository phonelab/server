import re
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.core.urlresolvers import reverse
from device.models import Device, DeviceProfile
from users.models import UserProfile
from datetime import datetime, timedelta

"""
Human Sorting
http://nedbatchelder.com/blog/200712/human_sorting.html
Sort log file name by time order

@date 02/20/2012

@author Kate Rhodes
@adder Taeyeon Ki
"""
"""
def tryint(s):
    try: 
        return int(s)
    except:
        return s
""" 
def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [int(c) if c.isdigit() else c for c in re.split('([0-9]+)', s) ] 

def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)

def re_sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)
    l.reverse()

"""
Login and Logout function to control session

@date 05/08/2012

@author Taeyeon Ki
"""
class ProtectedView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedView, self).dispatch(*args, **kwargs)
    
class AuthorProtectedView(ProtectedView):
    def dispatch(self, *args, **kwargs):
        post = self.get_queryset()
        
        if not post.author != self.request.user:
            return redirect('access_denied')
        
        return super(AuthorProtectedView, self).dispatch(*args, **kwargs)

"""
update working status using Last Log info

@date 07/16/2012

@author Taeyeon Ki
"""
def update_working_status():
  deviceprofiles = DeviceProfile.objects.all()

  for deviceprofile in deviceprofiles:
    if deviceprofile.last_log:
      if deviceprofile.last_log < (datetime.today() - timedelta(2)):
        #Not Working phone since a phone did not update a log file for two days
        DeviceProfile.objects.filter(id=deviceprofile.id).update(status="N")
      else:
        DeviceProfile.objects.filter(id=deviceprofile.id).update(status="W")


"""
check valid access

@date 07/18/2012
@param String user
@param String deviceId

@author Taeyeon
"""
def is_valid_device(user, deviceId):
  userprofile = UserProfile.objects.get(user_id=user.id)

  #to protect wrong accesses
  if userprofile.user_type == 'M' or userprofile.user_type == 'L':
    return DeviceProfile.objects.filter(group = userprofile.group).filter(dev=deviceId).count() > 0

  if userprofile.user_type == 'P':
    return DeviceProfile.objects.filter(dev=deviceId).filter(user=user).count() > 0
   
  if userprofile.user_type == 'A':
    return True
  return False
