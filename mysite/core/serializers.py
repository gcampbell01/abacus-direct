from io import StringIO
from django.db.models import Model
from django.db.models.query import QuerySet
from django.utils.encoding import smart_unicode
from django.utils.simplejson import dumps
from django.utils import simplejson
from datetime import datetime, date
from django.http import HttpResponse
from cgi import escape as cgiesc

"""
from serializers import to_json(data, **options)
"""

'''
# Some tests

>>> j = json_serialize
'''


def model_json(queryset, fields_tuple=None):
    from django.core import serializers as srl
    return srl.serialize('json', queryset, fields=fields_tuple)


def model_json_response(queryset, fields_tuple=None):
    data = model_json(queryset, fields_tuple)
    return HttpResponse(
        data,
        content_type='application/javascript; charset=utf8'
    )


def json_response(something):
    '''Turn something into JSON'''
    o = []
    o.append(something)
    return HttpResponse(
        simplejson.dumps(o),
        content_type='application/javascript; charset=utf8'
    )


def json_serialize(object, nested=False):
    '''
    set nested as true to return content of
    nested objects such as FK and m2m

    >>> from json import loads
    >>> from pprint import pprint
    >>> from core.serializers import json_serialize
    >>> x = Profile.objects.all()
    >>> s=json_serialize(x)
    >>> cs = loads(s)
    >>> pprint(cs)
    '''
    js = JSONSerializer()
    j = js.serialize(object, nested=nested)

    return j


def json_serialize_response(object, nested=False):
    r = json_serialize(object, nested)
    return HttpResponse(r, mimetype='application/json')


def to_json(data, **options):
    js = JSONSerializer()
    j = js.serialize(data, options)

    return j


class UnableToSerializeError(Exception):

    """ Error for not implemented classes """
    def __init__(self, value):
        self.value = value
        Exception.__init__(self)

    def __str__(self):
        return repr(self.value)

'''
If there are fields requiring serialization,
pass a list of SerializeEntities to
'''


class SerializeEntity():

    def __init__(self, search, replacement):
        self.needle = search
        self.replacement = replacement

    def __unicode__(self):
        return u'%s' % self.needle


class JSONSerializer():
    boolean_fields = ['BooleanField', 'NullBooleanField']
    datetime_fields = ['DatetimeField', 'DateField', 'TimeField']
    number_fields = ['IntegerField', 'AutoField',
                     'DecimalField', 'FloatField', 'PositiveSmallIntegerField']

    def serialize(self, obj, **options):
        self.options = options

        self.stream = options.pop("stream", StringIO())
        self.selectedFields = options.pop("fields", None)
        self.ignoredFields = options.pop("ignored", None)
        self.use_natural_keys = options.pop("use_natural_keys", False)
        self.transcript = options.pop("transcript", {})
        self.nested = options.pop('nested', False)
        self.currentLoc = ''

        # Placeholder for the later used parser
        self.html_parser = None

        # Escape all string information to be written to the output
        # stream though HTML parser, making it safe to transport.
        # Remove this feature for speed - warn; your JSON may be invalid if
        # False
        self.parse_html = options.pop('parse_html', False)

        # Stack recursive list.
        self.recurse_list = []

        self.level = 0

        self.start_serialization()

        self.handle_object(obj)

        self.end_serialization()
        return self.getvalue()

    def get_string_value(self, obj, field):
        """Convert a field's value to a string."""
        return smart_unicode(field.value_to_string(obj))

    def start_serialization(self):
        """Called when serializing of the queryset starts."""
        pass

    def end_serialization(self):
        """Called when serializing of the queryset ends."""
        pass

    def start_array(self):
        """Called when serializing of an array starts."""
        self.stream.write(u'[')

    def end_array(self):
        """Called when serializing of an array ends."""
        self.stream.write(u']')

    def start_object(self):
        """Called when serializing of an object starts."""
        self.stream.write(u'{')

    def end_object(self):
        """Called when serializing of an object ends."""
        self.stream.write(u'}')

    def handle_object(self, object):
        """ Called to handle everything, looks for the correct handling """
        if isinstance(object, dict):
            # Dictionaries will be called recurively.
            self.handle_dictionary(object)
        elif isinstance(object, list):
            # Each object is handled as an Object handle_object
            self.handle_list(object)
        elif isinstance(object, Model):
            # Handle a django model
            # Will call handle_m2m_field, handle_field, handle_fk_field
            self.handle_model(object)
        elif isinstance(object, QuerySet):
            # Handle django queryset
            # Each element is handled as a Django Model handle_model
            self.handle_queryset(object)
        elif isinstance(object, (bool, basestring, int, float, long)):
            # stringify and dump information
            self.handle_simple(object)
        elif isinstance(object, datetime):
            # Handles a datetime
            self.handle_datetime(object)
        elif isinstance(object, date):
            self.handle_date(object)
        elif object == None:
            self.handle_none(object)
        else:
            # If this a seralize entity
            try:
                self.handle_string(object)
            except Exception as e:
                raise UnableToSerializeError(type(object))

    def handle_dictionary(self, d):
        """Called to handle a Dictionary"""
        i = 0
        self.start_object()
        if isinstance(d, (dict, Model, QuerySet)):
            self.recurse_list.append(str(id(d)) + str(d))
            if(hasattr(d, '__dict__')):
                d.__dict__['__recursive__'] = str(id(d))
            else:
                d['__recursive__'] = str(id(d))

        for key, value in d.iteritems():
            self.currentLoc += key + '.'
            # self.stream.write(unicode(self.currentLoc))
            i += 1
            self.handle_simple(key)
            self.stream.write(u': ')

            _value = value
            # recursive care.
            ids = str(id(value)) + str(value)
            if ids not in self.recurse_list:
                if isinstance(value, (dict, Model, QuerySet)):
                    self.recurse_list.append(ids)
                self.handle_object(_value)
            else:

                _value = {
                    '__recursive__': self.safe_string(str(id(value))),
                }

                self.handle_object(_value)

            if i != len(d):
                self.stream.write(u', ')
            self.currentLoc = self.currentLoc[
                0:(len(self.currentLoc) - len(key) - 1)]
        self.end_object()

    def handle_list(self, l):
        """Called to handle a list"""
        self.start_array()

        c=0

        for value in l:
            self.handle_object(value)
            c+=1
            if c != len(l):
                self.stream.write(u', ')

        self.end_array()

    def handle_datetime(self, d):

        self.start_object()
        self.stream.write(u'"date" : "%s", ' % str(d))
        self.stream.write(u'"day" : "%s", ' % d.day)
        self.stream.write(u'"hour" : "%s", ' % d.hour)
        self.stream.write(u'"microsecond" : "%s", ' % d.microsecond)
        self.stream.write(u'"minute" : "%s", ' % d.minute)
        self.stream.write(u'"month" : "%s", ' % d.month)
        self.stream.write(u'"second" : "%s", ' % d.second)
        self.stream.write(u'"weekday" : "%s", ' % d.weekday())
        self.stream.write(u'"year" : "%s"' % d.year)

        self.end_object()

    def handle_date(self, d):

        self.start_object()
        self.stream.write(u'"day" : %s, ' % d.day)
        self.stream.write(u'"month" : %s, ' % d.month)
        self.stream.write(u'"year" : %s,' % d.year)
        self.stream.write(u'"weekday" : %s, ' % d.weekday())
        self.stream.write(u'"isoformat" : "%s", ' % d.isoformat())
        self.stream.write(u'"ctime" : "%s"' % d.ctime())

        self.end_object()

    '''
    from json import loads
    from pprint import pprint
    from core.serializers import json_serialize
    x = Profile.objects.all()
    s=json_serialize(x)
    cs = loads(s)
    pprint(cs)
    '''

    def handle_model(self, mod):
        """Called to handle a django Model"""

        try:
            _meta = mod._meta
        except AttributeError as e:
            _meta = None

        if _meta is None:
            # Try a standard object
            self.handle_simple(mod)
        else:
            self.start_object()
            for field in mod._meta.local_fields:
                if field.rel is None:
                    if self.selectedFields is None or field.attname in self.selectedFields or field.attname:
                        if self.ignoredFields is None or self.currentLoc + field.attname not in self.ignoredFields:
                            self.handle_field(mod, field)
                else:
                    if self.selectedFields is None or field.attname[:-3] in self.selectedFields:
                        if self.ignoredFields is None or self.currentLoc + field.attname[:-3] not in self.ignoredFields:
                            self.handle_fk_field(mod, field)
            for field in mod._meta.many_to_many:
                if self.selectedFields is None or field.attname in self.selectedFields:
                    if self.ignoredFields is None or self.currentLoc + field.attname not in self.ignoredFields:
                        self.handle_m2m_field(mod, field)
            self.stream.seek(self.stream.tell() - 2)
            self.end_object()

    def handle_queryset(self, queryset):
        """Called to handle a django queryset"""
        self.start_array()
        it = 0
        for mod in queryset:
            it += 1
            self.handle_model(mod)
            if queryset.count() != it:
                self.stream.write(u', ')
        self.end_array()

    def handle_field(self, mod, field):
        """Called to handle each individual (non-relational) field on an object."""
        self.handle_simple(field.name)
        if field.get_internal_type() in self.boolean_fields:
            if field.value_to_string(mod) == 'True':
                self.stream.write(u': true')
            elif field.value_to_string(mod) == 'False':
                self.stream.write(u': false')
            else:
                self.stream.write(u': undefined')
        else:
            self.stream.write(u': ')
            self.handle_simple(field.value_to_string(mod))
        self.stream.write(u', ')

    def handle_fk_field(self, mod, field):
        """Called to handle a ForeignKey field."""

        related = getattr(mod, field.name)
        if related is not None:
            if field.rel.field_name == related._meta.pk.name:
                # Related to remote object via primary key
                pk = related._get_pk_val()
            else:
                # Related to remote object via other field
                pk = getattr(related, field.rel.field_name)

            d = {
                'pk': pk,
            }
            if self.use_natural_keys and hasattr(related, 'natural_key'):
                d.update({'natural_key': related.natural_key()})
            if type(d['pk']) == str and d['pk'].isdigit():
                d.update({'pk': int(d['pk'])})

            self.handle_simple(field.name)
            self.stream.write(u': ')
            if self.nested:
                self.handle_model(related)
            else:
                self.handle_object(d)
            self.stream.write(u', ')

    def handle_m2m_field(self, mod, field):
        """Called to handle a ManyToManyField."""
        if field.rel.through._meta.auto_created:
            self.handle_simple(field.name)
            self.stream.write(u': ')
            self.start_array()
            hasRelationships = False

            # import pdb;pdb.set_trace()

            for relobj in getattr(mod, field.name).iterator():

                hasRelationships = True
                pk = relobj._get_pk_val()

                d = {
                    'pk': pk,
                }

                if self.use_natural_keys and hasattr(relobj, 'natural_key'):
                    d.update({'natural_key': relobj.natural_key()})
                if type(d['pk']) == str and d['pk'].isdigit():
                    d.update({'pk': int(d['pk'])})

                if self.nested:
                    self.handle_model(relobj)
                else:
                    self.handle_simple(d)
                self.stream.write(u', ')
            if hasRelationships:
                self.stream.seek(self.stream.tell() - 2)
            self.end_array()
            self.stream.write(u', ')

    def safe_string(self, strin):
        ''' Returns a transport ready string. '''
        esc = strin
        # UTF-8 save convert
        if type(strin) != unicode:
            esc = unicode('%s' % strin, "utf-8", errors="replace")
        esc = esc.replace('\n', '')

        # if to parse as HTML
        if self.parse_html:
            esc = cgiesc(esc).encode('ascii', 'xmlcharrefreplace')
        return unicode(esc)

    def handle_simple(self, simple):
        """ Called to handle values that can be handled via simplejson """
        esc = self.safe_string(dumps(simple))
        self.stream.write(esc)

    def handle_string(self, simple):
        esc = self.safe_string(simple)
        self.stream.write(u'"%s"' % esc)

    def handle_none(self, object):
        o = u'null'
        self.stream.write(o)  # unicode(dumps(o)))

    def getvalue(self):
        """Return the fully serialized object (or None if the output stream is  not seekable).sss """
        if callable(getattr(self.stream, 'getvalue', None)):
            return self.stream.getvalue()
