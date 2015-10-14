from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import os.path
import codecs
from django.db import models 
from django.db.models import Q
import sys
import csv # first we need import necessary lib:csv
import urllib2
from django.core import management
from amii.camera.models import Camera

class Command(BaseCommand):
    args = 'Something'
    help = 'Help content'
    
    
    def handle(self, *args, **options):
        qu = args[0]
        
        try:
            c = Camera.objects.get(Q(ip_address=qu)|
                               Q(name=qu))
            print "Resetting camera %s" % c
            
            ep = c.get_endpoint('UDPRebootCamera')
            
            print ep
            url = "http://%s%s" % (c.ip_address, ep.url)
            req = urllib2.urlopen(url)
            d = req.read()
            print d
        except Camera.DoesNotExist:
            print "Could not retrieve camera %s" % qu 
            
        #raise CommandError('Poll "%s" does not exist' % poll_id)
    