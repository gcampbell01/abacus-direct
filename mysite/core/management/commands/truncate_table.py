from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import os.path
import codecs
from django.db import models 
import sys
import csv # first we need import necessary lib:csv

class Command(BaseCommand):
    args = 'Something'
    help = 'Help content'
    option_list = BaseCommand.option_list + (
        make_option('--path', '-p', dest='path', default=False, help='Path of the CSV file'),
    )
    
    def handle(self, *args, **options):
        pass
        #raise CommandError('Poll "%s" does not exist' % poll_id)
    