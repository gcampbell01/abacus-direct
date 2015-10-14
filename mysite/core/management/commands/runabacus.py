from django.core.management.base import BaseCommand

from optparse import OptionParser, make_option
import os.path, sys, os
import runcpserver 
from runcpserver import runcpserver as rf

from termcolor import colored



CPSERVER_OPTIONS = {
'host': '0.0.0.0',
'port': 8008,
'server_name': 'localhost',
'threads': 10, 
'daemonize': False,
'workdir': os.path.abspath('..'), #back to the room of the app
'pidfile': None,
'server_user': 'www-data',
'server_group': 'www-data',
'ssl_certificate': None,
'ssl_private_key': None,
'autoenv': True, # If the env should be activated before start automatically.
'tools.staticdir.on': True,
'tools.staticdir.dir': os.path.join(os.path.abspath('..'), 'media'),
}


def start_server(options):
    """
    Start CherryPy server
    """    
    if options['daemonize'] and options['server_user'] and options['server_group']:
        #ensure the that the daemon runs as specified user
        change_uid_gid(options['server_user'], options['server_group'])
    
    from cherrypy.wsgiserver import CherryPyWSGIServer as Server
    from django.core.handlers.wsgi import WSGIHandler
    
    import cherrypy
    
    pth = os.path.join(os.path.abspath('..'), 'media')
    pth_ext = os.path.exists(pth)
    
    #MEDIA_ROOT = '/var/projects/%s:%s/media/' % (options['server_name'], int(options['port']) + 1)
    '''
    try:
        if pth_ext:
            MEDIA_ROOT = pth
        else:
            print "Media path is %s" % MEDIA_ROOT
    except: 
        print "Could not create dynamic MEDIA_ROOT path"
        print "%s is missing" % pth
    
    cherrypy.config['tools.staticdir.on']= True
    cherrypy.config['tools.staticdir.dir'] = pth
    '''
    
    server = Server(
        (options['host'], int(options['port'])),
        WSGIHandler(), 
        int(options['threads']), 
        options['server_name']
    )
    

    if options['ssl_certificate'] and options['ssl_private_key']:
        server.ssl_certificate = options['ssl_certificate']
        server.ssl_private_key = options['ssl_private_key']  
        #'tools.staticdir.on': True,
        #'tools.staticdir.dir': os.path.join(os.path.abspath('..'), 'media'),
    try:
        
        p('Starting server')
        server.start()
        #media_server.start()
        #from cherrypy.process.servers import ServerAdapter
        
        
        #s1 = ServerAdapter(cherrypy.engine, server)
        #s2 = ServerAdapter(cherrypy.engine, media_server)
        
        #s1.subscribe()
        #s2.subscribe()
        
        #cherrypy.engine.start()
    except KeyboardInterrupt:
        p('Stopping server')
        server.stop()
        #cherrypy.engine.stop()
        


        
def p(*a):
    for x in a:
        print x,
    print ' '

runcpserver.start_server = start_server
runcpserver.runcpserver = runcpserver

class Command(BaseCommand):
    option_list = runcpserver.Command.option_list
    help = runcpserver.Command.help
    args = runcpserver.Command.args
    
    def handle(self, *args, **options):
        
        c = CPSERVER_OPTIONS.copy()
        
        for x in args:
            if "=" in x:
                k, v = x.split('=', 1)
            else:
                k, v = x, True
            options[k.lower()] = v
        
        c.update(options)
        rf(**c)