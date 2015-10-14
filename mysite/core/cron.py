import kronos
import random
from django.conf import settings
from termcolor import colored
from amii.server.models import Connection
import sys
import subprocess
from django_cron import CronJobBase, Schedule
import os
from datetime import datetime

class TestCron(CronJobBase):
    RUN_EVERY_MINS = 1# every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'core.TestCron' # a unique code

    def do(self):
        f = open('TestCron-Output', 'a')
        dt = '%s\r\n' % str(datetime.now()) 
        f.write(dt)
        f.close()
        
def log(self, *args, **kargs):
    colors = (
      (bool, 'cyan'),
      (str, 'green'),
      (float, 'yellow'),
      (int, 'yellow'),
      (unicode, 'white'),
    )
    color = None
    if sys.stdin.isatty():
        color = kargs.get('color', None)
    i = 0
    # For each passed argument
    for a in args:
        i += 1
        if color is None:
            # Check if the user in attr
            if sys.stdin.isatty():
                # Loop through available colors
                #print ''
                col = color
                for t in colors:          
                    # Check to see if this type has many associated types
                    # (We're only interested in the first main type)
                    if hasattr(t[0], 'mro'):
                        i_t = t[0].mro()[0]
                    else:
                        i_t = t[0]
                   
                    # find and match color instance.
                    d = a
                    b = t[0] 
                    if str(d).isdigit():
                        b = int
                        d = int(d)
                    elif bool(d):
                        b = bool
                    
                    if isinstance(d, b):
                        col = t[1]
                sys.stdout.write(colored( str(a), col) )
            else:
                sys.stdout.write(str(a))
        else:
            sys.stdout.write(colored( str(a), color) )
        
        if len(args) == i:
             sys.stdout.write('\n')
        else:
             sys.stdout.write(' ')

# every minute, check the gateway is running, 
# Save a check to somewhere.
# Email developer
 
# @kronos.register('* * * * *') # < every minute
def checkgateway():
    '''Once a minute the gateway is checked to see if it's running.'''
    print colored("Check the gateway is running", color='white')
    
    connection = Connection.get_latest()
    c = connection
    #log("Process Name    ", c.process_name)
    #log("Running         ", c.running())
    
    if c.running() is not True:
        #start it.
        log('Gateway is not running, attempt restart.', color='red')
        
        c = [sys.executable, 'manage.py', 'runscript', 'recurse']
        
        log('running command', c)
        
        subprocess.Popen(c,  stdout=subprocess.PIPE, 
                            stderr=subprocess.STDOUT)
        
        connection = Connection.get_latest()
        c = connection
        
        '''
        log("Process Name    ", c.process_name)
        log("Running         ", c.running())
        log("Status (int)    ", c.status_int)
        log("Status (String) ", c.status_string)
        log("Status PID      ", c.pid)
        log("Status PPID     ", c.ppid)
        log("Endpoint Host   ", c.endpoint_host)
        log("Endpoint Port   ", c.endpoint_port)
        log("Create Time     ", c.create_time) 
        log("Connections     ", len(c.connections))
        '''

