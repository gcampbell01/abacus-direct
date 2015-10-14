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
    help = 'Help content'
    
    def handle(self, *args, **options):
        self.app_labels = []
        
        for a in args:
            print colored(a, 'red')
            app, file = self.make_file(a, 'views.py')
            print app, file
            self.write_lines(app, file)
            self.app_labels.append(a)
            file.close()
            
 
    
    def make_file(self, app_label, file_name):
        module, app = self.app_label_to_app_module(app_label)
        
        path = os.path.abspath(app.__file__)
        loc = path.split(os.path.sep)[:-1]
        loc = os.path.sep.join(loc)
        
        p = "%s%s%s" % (loc, os.path.sep, file_name)
        
        
        if os.path.isfile(p) is not True:
            file = open(p, 'w')
        else:
            self.say('%s file already exists' % file_name)
            exit(0)
        
        return app, file
  
  
        
    def write_lines(self, app, file):
        lines = ['from django.contrib import admin\n',
                'from django.http import HttpResponse\n',
                'from django.shortcuts import render_to_response\n',
                'from django.template import RequestContext\n',
                'from django.contrib.auth.decorators import login_required\n\n',
                'def context(request):\n',
                '    c = {}\n',
                'return c\n\n',
                '@login_required\n',
                'def index(request):',
                '    return render_to_response('dashboard.html', context_instance=RequestContext(request, processors=[context]))'
                ]
        
        for line in lines:
            file.write(line)
        
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
        