from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import os.path
import codecs
from django.db import models 
import sys
import csv # first we need import necessary lib:csv
'''
python manage.py csvimport --path /var/www/amii/csv/events.csv --model 'events.Event' -d ';' --mapping auto
python manage.py csvimport --path /var/www/amii/csv/events.csv --model 'events.Event' -d ';' --mapping autoprompt
'''

## {{{ http://code.activestate.com/recipes/577058/ (r2)
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.
    
    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":"yes",   "y":"yes",  "ye":"yes",
             "no":"no",     "n":"no"}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while 1:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return default
        elif choice in valid.keys():
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")
## end of http://code.activestate.com/recipes/577058/ }}}

def dictSort(d):
    """ returns a dictionary sorted by keys """
    our_list = d.items()
    our_list.sort()
    k = {}
    for item in our_list:
        k[item[0]] = item[1]
    return k

def is_int(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()

class Command(BaseCommand):
    args = 'Something'
    help = 'Help content'
    option_list = BaseCommand.option_list + (
        make_option('--path', '-p', dest='path', default=False, help='Path of the CSV file'),                                             
        make_option('--model', '-m', dest='model', default=False, help='The name of the model to insert the data'),
        make_option('--delimiter', '-d', dest='delimiter', default=',', help='Specify the delimiter of the CSV data'),
        make_option('--mapping', dest='mapping', default='prompt', help='Map the csv columns to the model fields')
    )
    
    path = None
    delim = ','
    
    mapping = None
    file = None
    reader = None
    
    def handle(self, *args, **options):
        
        path = options.get("path", None)
        self.delim = options.get('delimiter', None)
        self.mapping = options.get("mapping", None)
        
        model_name = options.get('model', False)
        file, self.reader = self.file_handler(path, args, options)
        modelclass = self.get_model(model_name, args, options)
        
        self.model_mapping(self.reader, modelclass, self.mapping, args, options)
    
    def model_mapping(self, csv_reader, model_class, model_mapping, *args, **options):
        '''
        map the models using the automated mapping system
        
        auto          The system will do it's best to map the data with comparison of fields and models
        manual        The layout specified by the presented information.
        prompt        The system will ask at each point - what model will be applied. 
        autoprompt    if auto fails, default to prompt.
        create a new models and import the fields based upon the provided 
        field names
        
        auto = Try to map the correct csv fields to the correct model fields by
        performing a dumb like to like mapping
        
        mapping = If mapping is provided, use the associated fields provided within
        the map to allocate the correct csv fields to the model.
        
        If these both fail, ask which fields are mapped to where.
        
        If failed - kill import
        '''
        method = model_mapping
        
        if method == 'auto':
            self.auto_model_mapping(model_class, model_mapping, args, options)
        elif method == 'autoprompt':
            self.autoprompt_mapping(model_class, csv_reader)
        elif method == 'prompt':
            self.autoprompt_mapping(model_class, csv_reader)
        else:
            '''manually typed mapping'''
            pass
            
    '''
    Perform user questioning and map the fields requested
    '''
    def autoprompt_mapping(self, model, csv_reader):
        model_fields = self.get_model_fields(model)
        csv_fields = self.get_csv_headers() 

        cor = 'no' # Correct
        while cor == 'no':
            maps = self.ask_mapping(model, csv_reader)
            
            print "" 
            print "Model".ljust(15), "<--".ljust(6), "CSV Fields"
            print "---------------------------------------------" 
            for map in maps:
                csv_value = maps[map] if maps[map] else ''
                print str(map).ljust(15), "<--".ljust(6), csv_value 
            
            cor = query_yes_no("Is this mapping correct? ", None)
            
            c = 0
            for row in self.reader:
                if c == 0:
                    header_map = self.get_csv_headers()
                else:
                    j=0
                    m = model()
                    for f in m.__dict__:
                        try:
                            ''' I know... I got to call it a symbiont_field! =D
                            The CSV field to collect '''
                            
                            symbiont_field = maps[f]
                            
                            if symbiont_field is not None:
                                d = row[header_map[symbiont_field]]
                                setattr(m, f, d.strip('"'))
    
                        except: 
                            d = "Unmatched"
                        j+=1    
                   
                    self.stdout.write("Saving model %s \n" % c)
                    m.save()
                c += 1
        #self._row_reader(model, maps, False, self._a, None)
        
        return maps
    
    def _a(self, maps, header_map, field, row, *args):
        if field.startswith("_"):
            pass
        else: 
            if maps is not None: 
                symbiont_field = maps[field] # =D Great name...
                print "symbiont_field %s" % symbiont_field 
                if symbiont_field is not None:
                    d = row[header_map[symbiont_field]]
            else:
                d = row[header_map[field]]
            return d
        
    def _b(self, maps, header_map, field, *args):
        if f.startswith("_"):
            #do not start with
            pass
        else:
            try:
                d = row[header_map[f]]
                setattr(m, f, d.strip('"'))
            except: 
                d = "Unmatched"
            j+=1
    '''
    When the corrected fields are found, pass to the external function.
    Allowing more control of how the data is mapped and stored into the database 
    '''
    def _row_reader(self, model, mapping=None, mask_models=False, func=None, *args):
        print '_row_reader'
        c = 0
        ''' Begin walking through the CSV '''
        for row in self.reader:
            if c == 0:
                ''' First request will fetch the real headers of the CSV '''
                header_map = self.get_csv_headers()
            else:
                j=0
                ''' Create a new instance of the model to save to. '''
                m = model()
                ''' Collect a field from the model, apply the collected model
                field and save the associated CSV data '''
                for f in m.__dict__:
                    
                    ''' Try to match the element specified within the passed function '''
                    if func:
                        ''' If the function exists, Call to its child. '''
                        d = func(mapping, header_map, f, row, args)
                        print "Return from function: %s" % d
                    else:
                        d = None
                        print 'D is none'
                    ''' Write this information to the model '''
                    setattr(m, f, d.strip('"'))
                
                    j+=1    
                else:
                    if f == 'id' and mask_models:
                        self.stdout.write("'%s' does not exist. This will be skipped.\n" % f)
                        
                #self.stdout.write("Saving model %s \n" % c)
                m.save()
            c += 1
    
        return mapping
            
    def auto_model_mapping(self, model, mapping_string, *args, **options):
        m = model()
        self.stdout.write("auto_model_mapping '%s'\n" % mapping_string)

        
        c = 0
        for row in self.reader:
            if c == 0:
                header_map = self.get_csv_headers()
            else:
                j=0
                m = model()
                for f in m.__dict__:
                    if f.startswith("_"):
                        #do not start with
                        pass
                    else:
                        try:
                            d = row[header_map[f]]
                            setattr(m, f, d.strip('"'))
                        except: 
                            d = "Unmatched"
                        j+=1    
                else:
                    if f is not 'id':
                        self.stdout.write("'%s' does not exist. This will be skipped.\n" % f)
                self.stdout.write("Saving model %s \n" % c)
                m.save()
            c += 1
            
    def get_model(self, model_name, *args, **options):

        if model_name is not False:
            return self._get_model(model_name)
        else:
            # Ask the user for the models.
            for x in self.all_models():
                s = str(x)
                n = s.replace("<class '", '')
                n = n.replace("'>", '')
                self.stdout.write('%s\n' % n)
            raw_model_name = raw_input('Enter the name of your model: ')
            return self._get_model(raw_model_name)
    
    def all_models(self):
        '''
        return a list of all available models
        '''
        return models.get_models()
        
    def _get_model(self, model_name):
            mn = model_name.split('.')
            '''
            the input here is based upon the internal Django modelling format.
            instead of 'amii.events.models.Event' You must use 'events.Event'
            '''
        
            modelclass = models.get_model(mn[0], mn[1])
            
            if modelclass is not None:
                return modelclass
            else:
                self.stdout.write("%s could not be imported. Specify model name like 'events.Event' - as per Django internal modelling.\n")
                
                raw_model_name = raw_input('Enter the name of your model: ')
                return self._get_model(raw_model_name)
            
                #raise CommandError("'%s' does not exist" % model_name)
    
    def file_handler(self, path, *args, **options): 
        file = None
        reader = None
        
      

        if path is False:
            import readline, glob
            
            # Give auto completion on the terminal!
            def complete(text, state):
                return (glob.glob(text+'*')+[None])[state]
            
            readline.set_completer_delims(' \t\n;')
            readline.parse_and_bind("tab: complete")
            readline.set_completer(complete)
            path = raw_input("Please specify the path of your file: ")
        
        self.path = path
        
        
        if os.path.isfile(path):
            self.stdout.write("Path is '%s'\n" % path)
            self.file = self.open_file(self.path)
            
            self.reader = csv.reader(self.file, delimiter= self.delim, quotechar='|')

        else:
            self.stdout.write('No CVS file path has been specified\n')
            self.file_handler(False)

        return self.file, self.reader
    
    def open_file(self, path):
        import codecs
        return codecs.open(path, 'r', "utf-8-sig")
        
    
    def get_model_fields(self, model_class):
        m = model_class()
        r = m.__dict__
        o = {}
        #field in row
        for f in r:
            if f.startswith("_"):
                #do not start with
                pass
            else:
               o[f] = r[f] 
        return o
    
    def get_csv_headers(self):
        c = 0
        self.file = self.open_file(self.path)
        csv_reader = csv.reader(self.file, delimiter= self.delim, quotechar='|')
        
        
        for row in csv_reader:
            #these are the row names 
            header_map = {}
            '''
            Map the header to the numerical associate.
            Later will be: header_map[0] == 'event_id'
            '''
            i = 0
            for h in row: 
                h = str(h).strip('"')
                header_map[h] = i 
                i += 1
            break
        return header_map

    

    def model_map(self, model, mapping_string, *args, **options):
        '''
        e.g: --mapping event_id=event_id, name=full_name, age=system_age
        CSV          model
        --------------------------
        event_id     event_id,
        name         full_name,
        age          system_age,
        '''
        
        '''Output data'''
        od = {}

        if mapping_string != 'auto':
            maps = mapping_string.split(',')
            for map in maps:
                m = map.split('=') 
                csv_field = m[0]
                model_field = m[1]

                if self.model_field_exists(model, model_field):
                    '''allow this'''
                    od[model_field] = csv_field
                else:
                    self.stdout.write("'%s' does not exist. Auto import will fail\n" % model_field)

            return od

    def model_field_exists(self, model, model_field_name):
        '''
        Check to see if this model field exists
        '''
        try:
            model.__dict__[model_field_name]
            return True
        except KeyError:
            return False

   
    
    def write_csv_field_list(self, csv_fields):
        
        i=0
        from operator import itemgetter
        
        x = sorted(csv_fields.items(), key=itemgetter(1))
        y = {}
        for k, v in x: 
            self.stdout.write("%s. %s\n" % (v + 1, k))
         

    def ask_mapping(self,model, csv_reader):
        model_fields = self.get_model_fields(model)
        csv_fields = self.get_csv_headers()
        
        map = {}
        
        self.write_csv_field_list(csv_fields)
        
        for model_field in model_fields:
            
            res = raw_input("Model field '%s' is mapped to (blank for no mapping): " % model_field)
            
            field = None
            
            ''' If the input is blank ''' 
            if res is not '':
                if is_int(res):
                    ''' A numerical was entered '''
                    index = int(res) - 1
                    field = self.get_csv_field_by_indicies(csv_fields, index)
                    if field is None:
                        print 'index %s is invalid' % res
                        return self.ask_mapping(model, csv_reader)
                    print "Selected (%s): '%s'" % (res, field)
                else:
                    ''' The typed form was entered
                    TODO: Reprompt for invalid input. '''
                    field = res
            else:
                pass
                #print 'Nothing entered'
            
            map[model_field] = field
        return map
   
    
    def get_csv_field_by_indicies(self, csv_fields, indices):
        for field in csv_fields: 
            if csv_fields[field] == indices:
                return field
        return None
        
