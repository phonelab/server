from django.http import HttpResponse
from lib.JSONSerializer import JSONSerializer

"""
JSON Response Helper

@date 01/31/2012
@param object response

@author Micheal
"""
def json_response_from(response):
  jsonSerializer = JSONSerializer()
  return HttpResponse(jsonSerializer.serialize(response, use_natural_keys=True), mimetype='application/json')