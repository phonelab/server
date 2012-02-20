#!/bin/sh
# phonelab - this script starts and stops the phonelab server
#
# chkconfig:   - 85 15
# description:  phonelab system using django gunicorn
#
# pidfile:     /home/ec2-user/server/8000.pid


ADDRESS='127.0.0.1'
PYTHON=`which python`
GUNICORN=`which gunicorn_django`
PROJECTLOC="/home/ec2-user/server"
MANAGELOC="$PROJECTLOC/manage.py"
DEFAULT_ARGS="--workers=3 --daemon --bind=$ADDRESS:"
BASE_CMD="$GUNICORN $DEFAULT_ARGS"

SERVER1_PORT='8000'
SERVER1_PID="$PROJECTLOC/$SERVER1_PORT.pid"

# Source function library.
. /etc/rc.d/init.d/functions

# Source networking configuration.
. /etc/sysconfig/network

# Check that networking is up.
[ "$NETWORKING" = "no" ] && exit 0

start_server () {
  if [ -f $1 ]; then
    #pid exists, check if running
    if [ "$(ps -p `cat $1` | wc -l)" -gt 1 ]; then
       echo "Server already running on ${ADDRESS}:${2}"
       return
    fi
  fi
  cd $PROJECTLOC
  echo "starting ${ADDRESS}:${2}"
  $BASE_CMD$2 --pid=$1
}

stop_server (){
  if [ -f $1 ] && [ "$(ps -p `cat $1` | wc -l)" -gt 1 ]; then
    echo "stopping server ${ADDRESS}:${2}"
    kill -9 `cat $1`
    rm $1
  else 
    if [ -f $1 ]; then
      echo "server ${ADDRESS}:${2} not running"
    else
      echo "No pid file found for server ${ADDRESS}:${2}"
    fi
  fi
}

case "$1" in
'start')
  start_server $SERVER1_PID $SERVER1_PORT 
  ;;
'stop')
  stop_server $SERVER1_PID $SERVER1_PORT
  ;;
'restart')
  stop_server $SERVER1_PID $SERVER1_PORT
  sleep 2
  start_server $SERVER1_PID $SERVER1_PORT
  ;;
*)
  echo "Django Project Init Usage: $0 { start | stop | restart }"
  ;;
esac

exit 0