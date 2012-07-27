from fabric.api import run, env, local, cd
import os

SSH_KEY_DIR = os.getenv('HOME') + '/.ssh/'

env.user = 'ec2-user'
env.key_filename = [os.path.join(SSH_KEY_DIR, "phonelab.pem")]

def staging():
  env.hosts = ['staging.phone-lab.org'] #107.22.187.240

def production():
  env.hosts = ['backend.phone-lab.org'] #107.20.190.88

def move():
  stop()
  run('/home/ec2-user/server/south.sh convert')
  run('rm -rf server')
  run("git clone git://github.com/phonelab/server.git")
  if os.environ.get("ENV") == "production":
    run("git checkout production")

def start():
  run('/etc/init.d/phonelab start')

def stop():
  run('/etc/init.d/phonelab stop')

def restart():
  start()
  stop()

def migrate():
  with cd('/home/ec2-user/server'):
#    run('python manage.py syncdb')
    run('/home/ec2-user/server/south.sh schemamigration')
    run('/home/ec2-user/server/south.sh migrate')

def deploy():
  move()
  migrate()
  restart()


## fab staging deploy

## if you want to syncdb
## fab move
## fab migrate
