# Create your views here.

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def download_manifest(request, phone_id):
  filename = ''.join(['/home/lsm5/manifests/', phone_id, '/manifest.xml'])
  return HttpResponse(open(filename).read(), 'text/plain')
