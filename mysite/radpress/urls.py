from django.conf.urls import patterns, url
from radpress.views import (
    ArticleArchiveView, ArticleDetailView, ArticleListView, PreviewView,
    PageDetailView, SearchView, ZenModeView, ZenModeUpdateView, TagListView,
    GenericTagListView, index)

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

    url(r'^detail/features/$',
        view=ArticleDetailView.as_view(),
        name='radpress-features'),

    url(r'^detail/solutions/$',
        view=ArticleDetailView.as_view(),
        name='radpress-solutions'),

    url(r'^detail/clients/$',
        view=ArticleDetailView.as_view(),
        name='radpress-clients'),

    url(r'^detail/about/$',
        view=ArticleDetailView.as_view(),
        name='radpress-about-us'),

    url(r'^detail/contact/$',
        view=ArticleDetailView.as_view(),
        name='radpress-contact'),
)
