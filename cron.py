#!/usr/bin/env python
#refer to http://bradmontgomery.blogspot.com/2009/02/scheduled-tasks-or-cron-jobs-with.html
from django.conf import settings
"""
Project-wide Cron Job... A Command-line Django Script.

This script gets scheduled and run by cron (or whatever).
It then calls the `run` method of each app's cron module, 
if it exists (should be `appname/cron.py`)

This script should be invoked after setting the 
DJANGO_SETTINGS_MODULE environment variable.

You should do this in a BASH script as follows:
    export DJANGO_SETTINGS_MODULE=mysite.settings
    python /path/to/mysite/cron.py
"""

def my_import(name):
  '''
  __import__ helper function to import modules inside packages
  e.g.:  where name is something like 'package.module.mod_i_want',
         would return mod_i_want
  
  See: http://www.python.org/doc/2.5.2/lib/built-in-funcs.html
  '''
  mod = __import__(name)
  components = name.split('.')
  for comp in components[1:]:
      mod = getattr(mod, comp)
  return mod

def run():
  for app in settings.INSTALLED_APPS:
    if not app.startswith('django'):
      output_info = '%s.cron'%app
      ## Dynamically import a module called 'cron'
      ## from each INSTALLED_APP (if it exists)
      try:
        cron_mod = my_import(app+'.cron')
        output_info += '... FOUND'
        print output_info
        ## 3. Execute the cron's run method (if it exists)
        if hasattr(cron_mod, 'run'):
          #print '---> calling run()'
          cron_mod.run()
      except ImportError:
      # ignore packages that don't have a cron module
        output_info += '... SKIPPED'
        print output_info

if __name__ == "__main__":
  run()
