from django.http import HttpResponse
from lib.JSONSerializer import JSONSerializer

"""
Return JSON 

@date 02/06/2012
@param object data

@author Micheal
"""
def json(data):
  jsonSerializer = JSONSerializer()
  return jsonSerializer.serialize(data)

"""
JSON Response Helper

@date 01/31/2012
@param object response

@author Micheal
"""
def json_response_from(response):
  jsonSerializer = JSONSerializer()
  return HttpResponse(jsonSerializer.serialize(response, use_natural_keys=True), mimetype='application/json')