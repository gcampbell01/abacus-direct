from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from django.core import management
from termcolor import colored
import threading, sys, time
from django.db import models
import os
import os.path
from django.db.models import loading

'''
loadfixtures app_name.model_name

    Look in model_name/fixtures for:
        initial_data.app_name.json

# Load fixtures for app
loadfixtures app_name 

# Load fictures for many apps
loadfixtures app_name app_name ...

# Mix and match app_names and single models
loadfixtures app_name app_name.model_name
    
# feed a file to it - same as loaddata
loadfixtures filename.json 

# feed many files to it - same as loaddata repeated
loadfixtures filename.json filename2.json ...

# feed a folder of fixtures
loadfixtures folder

# Feed many folders of fixtures
loadfixtures folder folder


# Load fixtures into app from file
loadfixtures app_name filename.json
loadfixtures app_name < filename.json

    
    Look for: 
    # Default
    model_name/fixtures/initial_data.json
    
    # The model name
    model_name/fixtures/initial_data.app_name.json
    
    # ALL apps for app_name
    model_name/fixtures/initial_data.app_name.model_name.json
    
    # alternative load location
    FIXTURES_ROOT/inital_data.app_name.json
    FIXTURES_ROOT/inital_data.app_name.model_namejson
    
    


# Pip a file to it
loadfixtures < filename.json
'''
class Command(BaseCommand):
    args = 'Model_Name'
    help = 'Load fixtures into django'
    
    def handle(self, *args, **options):
        pass