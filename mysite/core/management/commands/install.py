#install
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from django.core import management
from termcolor import colored
import threading, sys, time
from django.db import models
import os
import os.path
from django.db.models import loading

class Command(BaseCommand):
    args = 'Model_Name'
    help = 'Install abacus.'
    
    def handle(self, *args, **options):
        self.app_labels = []
        
        # create env
        # fetch application
        # install apt-get requirements
        
        # syncb
        # perform migrate
        # load json
        # install crons
     
    def say(self, *args):
            s = ''
            c= ''
            for x in args:
                s += "%s%s" % (c, x)
                c = ', '
            print(s)

    def ask(self, q):
        inp = raw_input(q)
        
        if inp in ['yes', 'ye', 'y' ]:
            return True
        elif inp in ['no', 'n']:
            return False
        else:
            print "Input not correct, answer Y/N"
            self.ask(q)
