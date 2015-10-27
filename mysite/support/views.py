
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from context import context
from forms import CustomMessageForm
from django.forms.models import inlineformset_factory
from django.conf import settings
from django.contrib.auth.models import User
from models import Email

def index(request):
    '''
    The form will be a model field, 
    the user field will be a singular.
    the emails to field can be many.
    The visuals will be standard clean.
    '''
    users = User.objects.all()
    recipient = users[0]
    message = None
    saved = False

    
    if request.method == 'POST':
        c = CustomMessageForm(request.POST)

        if c.is_valid():
            #save
            sn = c.cleaned_data['sender_name']
            se = c.cleaned_data['sender_email']
            rn = recipient.username
            re = recipient.email
            s = c.cleaned_data['subject']
            b = c.cleaned_data['body']
            
            e, cr = Email.objects.get_or_create(name=sn, email=se)
            e.save()
            
            e1, cr = Email.objects.get_or_create(name=rn, email=re)
            e1.save()
            e.send()
            
            saved=True
            message = 'Cheers.'
        else:
            message = 'Some items need checking'
    else:
        c = CustomMessageForm()
        #not valid
    
    return render_to_response('support/index.html', {'form': c, 
                                                     'message': message, 
                                                     'saved': saved
                                                     },
                context_instance=RequestContext(request, processors=[context]))
    #return HttpResponse(request) 
