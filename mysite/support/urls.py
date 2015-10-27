from django.conf.urls import *

urlpatterns = patterns('support.views',
    url(r'^$', 'index', name='support_index'),
    url(r'^post/$', 'index', name='support_post'),
    
)