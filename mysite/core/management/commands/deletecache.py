from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import os.path
import codecs
from django.db import models 
import sys, os
import csv # first we need import necessary lib:csv
from django.core import management
from subprocess import call, check_call, Popen
from termcolor import colored
import threading, sys, time
from amii.events.models import CountCache


class Command(BaseCommand):
    args = 'Something'
    help = 'Help content'
    
    def handle(self, *args, **options):
        s = "\n************************************************************ \
            \n* Deleting the count cache is not an action to be taken    * \
            \n* lightly. By doing this, Abacus will cry a little as it   * \
            \n* populates the cache again.                               * \
            \n************************************************************" 
        print colored(s, 'red')
        a = self.ask("Are you sure you wish to continue (y/n): ")
        
        if a:
            CountCache.objects.all().delete()
            print "Total remaining: %s" % CountCache.objects.count()
            
        #management.call_command('runscript', 'server')
        #eval("management.call_command('runscript', 'server')") 
        #raise CommandError('Poll "%s" does not exist' % poll_id)
    
    def ask(self, q):
        inp = raw_input(q)
        
        if inp in ['yes', 'ye', 'y' ]:
            return True
        elif inp in ['no', 'n']:
            return False
        else:
            print "Input not correct, answer Y/N"
            self.ask(q)
        