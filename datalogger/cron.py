from utils import update_working_status

"""
Cron Job that checks the LastLog file to update phone status info to the db

@date 12/10/2011
@param String deviceId

@author TKI
"""
#class CheckLastLog(Job):

# run every 300 seconds (5 minutes)
#  run_every = 300
                
#  def job(self):
   # This will be executed every 5 minutes
#    update_working_status()

#cronScheduler.register(CheckLastLog)

def run():
  update_working_status()
