from django.conf.urls import patterns, url
from radpress.views import (
    ArticleArchiveView, ArticleDetailView, ArticleListView, PreviewView,
    PageDetailView, SearchView, ZenModeView, ZenModeUpdateView, TagListView,
    GenericTagListView, index, users, reports, alerts, museums, privacy)

from radpress.feeds import ArticleFeed

urlpatterns = patterns(
    'radpress.views',

    #url(r'^$',
    #    view=TagListView.as_view(),
    #    name='radpress-article-list'),

    url(r'^$', 'index', name='radpress_home'),

    url(r'^tags/$',
        view=ArticleArchiveView.as_view(),
        name='radpress-article-tags'),

    url(r'^archives/$',
        view=GenericTagListView.as_view(),
        name='radpress-article-archive'),

    url(r'^detail/(?P<slug>[-\w]+)/$',
        view=ArticleDetailView.as_view(),
        name='radpress-article-detail'),

    url(r'^p/(?P<slug>[-\w]+)/$',
        view=PageDetailView.as_view(),
        name='radpress-page-detail'),

    url(r'^preview/$',
        view=PreviewView.as_view(),
        name='radpress-preview'),

    url(r'^search/$',
        view=SearchView.as_view(),
        name='radpress-search'),

    url(r'^zen/$',
        view=ZenModeView.as_view(),
        name='radpress-zen-mode'),

    url(r'zen/(?P<pk>\d+)/$',
        view=ZenModeUpdateView.as_view(),
        name='radpress-zen-mode-update'),

    url(r'^rss/$',
        view=ArticleFeed(),
        name='radpress-rss'),

    url(r'^rss/(?P<tags>[-/\w]+)/$',
        view=ArticleFeed(),
        name='radpress-rss'),

    #url(r'^$',
        #view=ArticleListView.as_view(),
        #name='radpress-article-list'),

    url(r'^detail/home/$',
        view=ArticleDetailView.as_view(),
        name='radpress-home'),

    #url(r'^detail/features/$',
    #    view=ArticleDetailView.as_view(),
    #    name='radpress-features'),

    url(r'^detail/solutions/$',
        view=ArticleDetailView.as_view(),
        name='radpress-solutions'),

    url(r'^detail/clients/$',
        view=ArticleDetailView.as_view(),
        name='radpress-industries'),

    url(r'^detail/about/$',
        view=ArticleDetailView.as_view(),
        name='radpress-about-us'),

    url(r'^detail/contact/$',
        view=ArticleDetailView.as_view(),
        name='radpress-contact'),

    # Features pages

    url(r'features/$',
        'features',
        name='radpress-features'),

    url(r'^features/users/$',
        'users',
        name='radpress-users'),
    
    url(r'^features/live/$',
        'live',
        name='radpress-live'),
    
    url(r'^features/reports/$',
        'reports',
        name='radpress-reports'),
    
    url(r'^features/auto/$',
        'auto',
        name='radpress-auto'),

    url(r'^features/alerts/$',
        'alerts',
        name='radpress-alerts'),

    # Industries
    
    url(r'^industries/retail/$',
        'retail',
        name='radpress-retail'),
    
    url(r'^detail/home/$',
        view=ArticleDetailView.as_view(),
        name='radpress-local'),
    
    url(r'^detail/home/$',
        view=ArticleDetailView.as_view(),
        name='radpress-wan'),
    
    url(r'^detail/home/$',
        view=ArticleDetailView.as_view(),
        name='radpress-cloud'),

    
    url(r'^industries/museums/$',
        "museums",
        name='radpress-museum'),
    
    url(r'^detail/home/$',
        view=ArticleDetailView.as_view(),
        name='radpress-carpark'),
    
    url(r'^detail/home/$',
        view=ArticleDetailView.as_view(),
        name='radpress-airport'),

    url(r'^privacy-policy/$',
        'privacy',
        name='radpress-privacy'),
)
