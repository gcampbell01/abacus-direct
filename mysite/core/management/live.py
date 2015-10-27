from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import os.path
import codecs
from django.db import models 
import sys, os
import csv # first we need import necessary lib:csv
from django.core import management
from subprocess import call, check_call, Popen
import time

class Command(BaseCommand):
    args = 'Something'
    help = 'Help content'
    
    def start(self):
        c = ['python', 'manage.py', 'runscript', 'server', '&']
        check_call(c)
        
        print "After c"
        while True:
            time.sleep(1)
            con = Connection.get_latest()
            print con, self.con
            
    
    def handle(self, *args, **options):
        from amii.server.models import Connection
        self.con = Connection.get_latest()
        # Get the last running connection
        if con.running is not True:
            try:
                s = self.start()
            except KeyboardInterrupt:
                print "SERVER DID NOT START"
        
        # Check to see if it is running
            # If running
                # pass
            # else
                # start gateway
        print "Calling command"
        
        #management.call_command('runscript', 'server')
        #eval("management.call_command('runscript', 'server')") 
        #raise CommandError('Poll "%s" does not exist' % poll_id)
    