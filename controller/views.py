import os
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def download_manifest(request, phone_id):
  manifest_file = ''.join([os.getenv('HOME'), '/manifests/', phone_id, '/manifest.xml'])
  return HttpResponse(open(manifest_file).read(), 'text/plain')
