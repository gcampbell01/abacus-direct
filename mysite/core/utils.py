import re
from crontab import CronTab

def error_content(type, value, tb):
    value = str(value)
    match = re.search(r"\[Errno (?P<number>(.*\d))\] (?P<string>([^\r].*))", value, re.IGNORECASE)
    err_num = None
    message = None
    
    if match:
        err_num = match.group("number")
        message = match.group("string")
    else:
        message = ""
        
    if err_num:
        err_num = int(err_num)
        
    return (err_num, message)


def overload(o, s, v, pushing=False, push_branch='__pushed'):
 
    '''
    Push support moves an existing
    branch to a new node before an object is written 
    called __push
    '''
    split = s.split('.')
    obj = o
    count = len(split)
    i = 0
    made = False;
    for x in split:
        i += 1 
        
        xs = str(x)
        #print 'looking at', xs, 'in', o
        if x in obj and made is False:
            #print x, 'in object'
            # Thats good. we go into that to search the next child.
            #if isinstance(obj[xs],object): 
            if hasattr(obj[xs], '__iter__') and isinstance(obj[xs],object):
                if i == count:
                    #print 'Writing new value', v
                    obj[xs] = v
                else:
                    obj = obj[xs]
            else:
                # we've reached the end of the line and 
                # anything beyond this is scrapped
                # or overloaded.
                # In this case, we rewrite the current object
                # print "Hit", type(obj[xs])
                d = obj[xs]
                if pushing:
                    obj[xs] = { push_branch: d}
                else:
                    obj[xs] = d
                obj = obj[xs] 
        else:
            #print 'making', x
            # nope. We make that node.
            obj[xs] = {}
            
            made = True;
            
            if count == i:
                # last Item in list is given a value.
                obj[xs] = {}
                obj[xs] = v
                #print 'gave', x, 'value of ', v
            else:
                #print 'step into', x
                obj = obj[xs]
    return obj

'''
o = { 'company': {}, 'people': 9}

overload(o, 'company.details.name', 'StrangeMother')
overload(o, 'company.details.contact_details', 'email@email.com')
overload(o, 'company.details.contact_details.name', 'tom')
overload(o, 'company.details.contact_details.name.lastname', 'thumb', pushing=True, push_branch='firstname')
overload(o, 'employees_unsafe.1', 'Bob')
overload(o, 'employees_unsafe.1', 'Dave')
overload(o, 'employees_unsafe.2', 'Mike')
overload(o, 'employees_unsafe.3', 'Flad')
overload(o, 'employees_unsafe.another', 'Him')
overload(o, 'employees_safe', None, pushing=True)

overload(o, 'employees_safe.1', {'name': 'Bob'}, pushing=True)
overload(o, 'employees_safe.1', {'name': 'Dave'}, pushing=True)
overload(o, 'employees_safe.2', {'name': 'Bob'}, pushing=True)
overload(o, 'employees_safe.3', {'name': 'Eric'}, pushing=True)
overload(o, 'employees_safe.4', {'name': 'Sainy'}, pushing=True)
overload(o, 'employees_safe.5', {'name': 'Jay'}, pushing=True)
overload(o, 'employees_safe.6', {'name': 'Sladge'}, pushing=True)
overload(o, 'employees_safe.7', {'name': 'Timmy'}, pushing=True)
overload(o, 'employees_safe.1', {'name': 'Other guy'}, pushing=True)

overload(o, 'employees_unsafe.1', {'name': 'Bob'})
overload(o, 'employees_unsafe.1', {'name': 'Dave'})
overload(o, 'employees_unsafe.2', {'name': 'Bob'} )
overload(o, 'employees_unsafe.3', {'name': 'Eric'})
overload(o, 'employees_unsafe.4', {'name': 'Sainy'})
overload(o, 'employees_unsafe.5', {'name': 'Jay'})
overload(o, 'employees_unsafe.6', {'name': 'Sladge'})
overload(o, 'employees_unsafe.7', {'name': 'Timmy'})
overload(o, 'employees_unsafe.1', {'name': 'Other guy'})
from pprint import pprint
pprint( o)

'''

# Calculating 
class CronProxy(object):
    ''' Cron proxy will write to model, cron - with attributes to
    identify all.
    Commands will be auto wrapped with the django env setup, valid crons
    will only be those targeting a management command.'''

    def create(self, command):
        '''Create a cron'''
        cron_model = CronRegister(command=command)
        cron_model.save()

        crontab = CronTab()
        comment = 'Auto Create by Abacus #%s' % cron_model.pk
        job = crontab.new(command=command, comment=comment)
