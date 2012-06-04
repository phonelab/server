from os.path import join
from django.conf import settings
from django.template import TemplateDoesNotExist
from mobile_utils import MOBILE_TEMPLATES_DIR
from mobile_utils.middleware import get_current_request


def load_template_source(template_name, template_dirs=None):
  request = get_current_request()
  if hasattr(request, 'is_mobile') and request.is_mobile:
    for path in MOBILE_TEMPLATES_DIR:
      try:
        filepath = join(path, template_name)
        file = open(filepath)
        try:
          return (file.read(), filepath)
        finally:
          file.close()
      except IOError:
        pass
  raise TemplateDoesNotExist(template_name)
load_template_source.is_usable = True
