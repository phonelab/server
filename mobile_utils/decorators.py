from django_mobile_utils import flag_request_for_mobile

def is_mobile(view):
#Django View Decorator
  def check_for_mobile_request(request, *args, **kwargs):
    flag_request_for_mobile(request)
    return view(request, *args, **kwargs)
  return check_for_mobile_request
