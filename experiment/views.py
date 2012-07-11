from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from users.models import UserProfile

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
