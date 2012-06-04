import re, os
from django.conf import settings

class ConfigurationException(Exception):
  pass

DMU_PATH = os.path.dirname(__file__)

dmu_settings = getattr(settings, 'MOBILE_UTILS_SETTINGS', None)
if not dmu_settings:
  raise ConfigurationException("settings file missing MOBILE_UTILS_SETTINGS")
IGNORE_LIST = dmu_settings.get('IGNORE_LIST', ())
MOBILE_TEMPLATES_DIR = dmu_settings.get('MOBILE_TEMPLATES_DIR', ())
USE_REGEX = dmu_settings.get('USE_REGEX', False)
USER_AGENTS_FILE = dmu_settings.get('USER_AGENTS_FILE', False)
USE_VERSION_REGEX = dmu_settings.get('USE_VERSION_REGEX', False)

def load_from_agents_file():
  f = None
  try:
    if USER_AGENTS_FILE:
      f = open(USER_AGENTS_FILE)
    else:
      f = open(os.path.join(DMU_PATH, 'data/' 'mobile_agents.txt'))
    ss = f.readlines()
  finally:
    if f:
      f.close()
  return [s.strip() for s in ss if not s.startswith('#') and s not in IGNORE_LIST]

USER_AGENTS = load_from_agents_file()
browser_regexs = [re.compile(s, re.I|re.M) for s in USER_AGENTS]
version__regex = re.compile(r"1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\\-(n|u)|c55\\/|capi|ccwa|cdm\\-|cell|chtm|cldc|cmd\\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\\-s|devi|dica|dmob|do(c|p)o|ds(12|\\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\\-|_)|g1 u|g560|gene|gf\\-5|g\\-mo|go(\\.w|od)|gr(ad|un)|haie|hcit|hd\\-(m|p|t)|hei\\-|hi(pt|ta)|hp( i|ip)|hs\\-c|ht(c(\\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\\-(20|go|ma)|i230|iac( |\\-|\\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\\/)|klon|kpt |kwc\\-|kyo(c|k)|le(no|xi)|lg( g|\\/(k|l|u)|50|54|e\\-|e\\/|\\-[a-w])|libw|lynx|m1\\-w|m3ga|m50\\/|ma(te|ui|xo)|mc(01|21|ca)|m\\-cr|me(di|rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\\-2|po(ck|rt|se)|prox|psio|pt\\-g|qa\\-a|qc(07|12|21|32|60|\\-[2-7]|i\\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\\-|oo|p\\-)|sdk\\/|se(c(\\-|0|1)|47|mc|nd|ri)|sgh\\-|shar|sie(\\-|m)|sk\\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\\-|v\\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\\-|tdg\\-|tel(i|m)|tim\\-|t\\-mo|to(pl|sh)|ts(70|m\\-|m3|m5)|tx\\-9|up(\\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|xda(\\-|2|g)|yas\\-|your|zeto|zte\\-", re.I|re.M)


def flag_request_for_mobile(request):
  request.is_mobile = False
  if 'opera mini' not in IGNORE_LIST and request.META.has_key("HTTP_X_OPERAMINI_FEATURES"):
    #opera mini.
    # http://dev.opera.com/articles/view/opera-mini-request-headers/
    request.is_mobile = True
    return request

  if 'wap' not in IGNORE_LIST and request.META.has_key("HTTP_ACCEPT"):
    s = request.META["HTTP_ACCEPT"].lower()
    if 'application/vnd.wap.xhtml+xml' in s:
      # Then it's a wap browser
      request.is_mobile = True
      return request

  if request.META.has_key('HTTP_USER_AGENT'):
    user_agent = request.META['HTTP_USER_AGENT']
    if USE_REGEX:
      for br in browser_regexs:
        if br.search(user_agent):
          request.is_mobile = True
          return request
      if USE_VERSION_REGEX and version__regex.search(user_agent[0:4]):
        request.is_mobile = True
        return request
    else:
      for ua in USER_AGENTS:
        if ua in user_agent:
          request.is_mobile = True
  return request
