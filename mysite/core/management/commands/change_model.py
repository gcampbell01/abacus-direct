from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from django.core import management
from termcolor import colored
import threading, sys, time
from django.db import models
import os
import os.path
from django.db.models import loading

from south.migration.base import Migration, Migrations

class Command(BaseCommand):
    args = 'Model_Name'
    help = 'Help content'
    
    def handle(self, *args, **options):
        self.app_labels = []
        
        for a in args:
            print colored(a, 'red')
            p = self.get_admin(a)
            s = unicode(a)
            
            l = self.app_label_to_app_module(a)[0]
            
            print 'Performing South schema migration'
            has_migrations = hasattr(l, 'migrations')
            
            if has_migrations:
                print "Performing auto migration"
                management.call_command('schemamigration', l, auto=True)
            else:
                print 'Performing init migration'
                management.call_command('schemamigration', l,auto=False, initial=True)
            
            
            
            print 'Performing South migration'
            management.call_command('migrate', l)
            #migrations = Migrations(l, force_creation=True, verbose_creation=verbosity > 0)
            
            f = self.file_head(p)
         
            if f[0] == '# Auto Generated with make_admin\n':
                print 'writing admin.py'
                os.unlink(p)
                management.call_command('make_admin', a)
    
    def file_head(self, file_name, lines=1):

        with open(file_name) as myfile:
            head=[myfile.next() for x in xrange(lines)]
        
        return head
                    
    def get_app_label(self,app):
        """
        Returns the _internal_ app label for the given app module.
        i.e. for <module django.contrib.auth.models> will return 'auth'
        """
        return app.__name__.split('.')[-2]


    def app_label_to_app_module(self, app_label):
        """
        Given the app label, returns the module of the app itself (unlike models.get_app,
        which returns the models module)
        """
        # Get the models module
        app = models.get_app(app_label)
        module_name = ".".join(app.__name__.split(".")[:-1])
        try:
            module = sys.modules[module_name]
        except KeyError:
            __import__(module_name, {}, {}, [''])
            module = sys.modules[module_name]
        return module, app
       
    def get_admin(self,app_label):
        return self.get_abs_path(app_label, 'admin.py')
        
    def get_abs_path(self, app_label, file_name):
        module, app = self.app_label_to_app_module(app_label)
        
        path = os.path.abspath(app.__file__)
        loc = path.split(os.path.sep)[:-1]
        loc = os.path.sep.join(loc)
        
        p = "%s%s%s" % (loc, os.path.sep, file_name)
        
        return p
            
    def ask(self, q):
        inp = raw_input(q)
        
        if inp in ['yes', 'ye', 'y' ]:
            return True
        elif inp in ['no', 'n']:
            return False
        else:
            print "Input not correct, answer Y/N"
            self.ask(q)
        