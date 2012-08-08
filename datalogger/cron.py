from utils import update_working_status

"""
Cron Job that checks the LastLog file to update phone status info to the db

@date 12/10/2011
@param String deviceId

@author TKI
"""
def run():
  update_working_status()
