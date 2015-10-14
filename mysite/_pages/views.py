from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.utils.decorators import method_decorator
from django.views.generic import (
    ArchiveIndexView, DetailView, FormView, ListView, TemplateView, UpdateView,
    View)
from radpress.mixins import (
    BaseViewMixin, EntryViewMixin, JSONResponseMixin, TagViewMixin,
    ZenModeViewMixin)
from radpress import settings as radpress_settings
from pages.models import Article, EntryImage, Page, Tag, ArticleTag
from radpress.readers import get_reader
#from django.template import context


class ArticleListView(BaseViewMixin, TagViewMixin, ListView):
    model = Article
    template_name = 'articletag_list.html'

    def get_queryset(self):
        ap = self.model.objects.all_published()[:radpress_settings.LIMIT]
        return ap

    def get_context_data(self, **kwargs):
        c = context(self.request)
        data = super(ArticleListView, self).get_context_data(**kwargs)

        data.update({'by_more': True})
        c.update(**data)
        return c


class ArticleDetailView(
        BaseViewMixin, TagViewMixin, EntryViewMixin, DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        c = {}
        #import pdb;pdb.set_trace()
        #data = super(ArticleDetailView, self).get_context_data(**kwargs)

        #data.update({'by_more': True})
        #c.update(**data)
        c.update(**kwargs)

        #c['object'].weight += 1
        #c['object'].save()

        return c


class PageDetailView(BaseViewMixin, TagViewMixin, EntryViewMixin, DetailView):
    model = Page


class GenericTagListView(BaseViewMixin, TagViewMixin, ListView):
    model = Tag
    template_name = 'radpress/generic_article_list.html'

    def get_queryset(self):
        queryset = self.model.objects.all()

        # filter for tags, if possible...
        tag = self.request.GET.get('tag')
        # import pdb;pdb.set_trace()
        if tag == 'other':
            # Use the other class view, 
            queryset = TagListView().get_queryset(['other'])
            # Alt list uses fields  created by the smart list generator.
            # Thusly, the queryset requires the template designed for it's data 
            # shape
            self.template_name = 'radpress/articletag_list_alt.html'
        elif tag:
            queryset = queryset.filter(slug=tag)

        return queryset

    def get_context_data(self, **kwargs):
        c = context(self.request)
        data = super(GenericTagListView, self).get_context_data(**kwargs)

        data.update({'by_more': True})
        c.update(**data)
        return c



class ArticleArchiveView(BaseViewMixin, TagViewMixin, ArchiveIndexView):
    model = Article
    date_field = 'created_at'
    paginate_by = 25

    def get_queryset(self):
        queryset = self.model.objects.all_published()

        # filter for tags, if possible...
        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tags__slug=tag)

        return queryset

    def get_context_data(self, **kwargs):
        c = context(self.request)
        data = super(ArticleArchiveView, self).get_context_data(**kwargs)
        data.update({
            'enabled_tag': self.request.GET.get('tag')
        })
        c.update(**data)

        return c


class SearchView(BaseViewMixin, TemplateView):
    template_name = 'radpress/search.html'
    models = (Article, Page)

    def get_queryset(self):
        queryset = []       
        q = self.request.GET.get('q')

        if not q:
            return queryset

        for model in self.models:
            queryset += model.objects.filter(
                Q(title__icontains=q) | Q(slug__icontains=q) |
                Q(content__icontains=q), is_published=True)

        return queryset

    def get_context_data(self, **kwargs):
        c = context(self.request)
        data = super(SearchView, self).get_context_data(**kwargs)
        data.update({'object_list': self.get_queryset()})

        c.update(**data)

        return c


class PreviewView(JSONResponseMixin, View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PreviewView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        content = request.POST.get('content', '')
        markup = request.POST.get('markup')
        reader = get_reader(markup=markup)
        content_body, metadata = reader(content).read()
        image_id = metadata.get('image', '')
        try:
            image_url = EntryImage.objects.get(id=int(image_id)).image.url
        except (EntryImage.DoesNotExist, ValueError):
            image_url = ''

        context = {
            'content': content_body,
            'title': metadata.get('title'),
            'tags': list(metadata.get('tags', [])),
            'image_url': image_url
        }

        return self.render_to_response(context)


class ZenModeView(ZenModeViewMixin, FormView):
    pass


class ZenModeUpdateView(ZenModeViewMixin, UpdateView):
    model = Article


class TagListView(ListView):
    template_name = 'pages/articletag_list.html'
    models = (Tag, Article)

    def get_queryset(self):
        '''
        tag_list = self.models[0].objects.all()
        # filter for tags, if possible...
        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tags__slug=tag)
        tags = tag_list.annotate(num_art=Count('article'))

        return tags.order_by('-num_art')
        '''
        return Article.objects.all()

    def get_tag_count(self):
        article_list = self.models[1].objects.all()
        arts = article_list.annotate(num_tag=Count('tags'))
        '''
        pseudo:
        if an article has more than 1 tag:
            assign only the tag with the highest num_tag
            assign that tag as the priority tag.

        then use that priority tag to display on the template
        '''
        for key in arts:
            if key.num_tag >= 2:
                key.p_tag = key.tags.all()[0]
            else:
                key.p_tag = key.tags.all()[0]

        #import pdb;pdb.set_trace()

        return arts


    def get_context_data(self, **kwargs):
        c = {}
        data = super(TagListView, self).get_context_data(**kwargs)
        #data.update({'object_list': self.get_queryset(), 'tag_count': self.get_tag_count()})
        data.update({'object_list': self.get_queryset()})

        c.update(**data)
        return c
        

#from pprint import pprint
"""class TagListView(ListView):
    #template_name = 'radpress/articletag_list.html'
    template_name = 'pages/articletag_list_alt.html'
    model = Article

    def get_queryset(self, selected=None):
        '''
        Return a smart list style order of the articles.
        Any article with low value association is added to
        an 'other' list.

        pass a list of strings in selected, to choose which tag + articles 
        to return. Any tag name missing from the list will be ommited

        >>> TagListView.get_queryset(['other', 'report', 'install'])
        
        '''
        articles = Article.objects.filter(is_published=True)
        used_articles = []
        tag_list = {}
        for article in articles:
            #import pdb;pdb.set_trace()
            #tag_count = article.tags.count()
            acount = 0
            #if tag_count == 1:
            #     acount = article.tags.all()[0].article_set.count()

            if acount == 1:
                tag = article.tags.all()[0]
                #print tag, article
                #import pdb;pdb.set_trace()
               
                if tag.name in tag_list:
                    
                    if selected:
                        if tag.name in selected:
                            tag_list[tag.name]['articles'].append(article)
                    else:
                        tag_list[tag.name]['articles'].append(article)

                else:
                    if 'other' not in tag_list:
                        tag_list['other'] = {
                            'tag': tag,
                            'articles': []
                        }

                    if selected:
                        if 'other' in selected:
                            tag_list['other']['articles'].append(article)
                    else:
                        tag_list['other']['articles'].append(article)

                used_articles.append(article)
            else:
                # more than one tag
                tags = article.tags.all()
                f_tag = None

                for tag in tags:
                    if not f_tag: f_tag = tag
                    ac = tag.article_set.count()
                    if ac > f_tag.article_set.count():
                        f_tag = tag

                if f_tag:

                    make_tag = f_tag.name not in tag_list
                    if selected and f_tag.name not in selected:
                            make_tag = False
                    if make_tag:
                        tag_list[f_tag.name] = {
                            'tag': tag,
                            'articles': []
                        }

                    used_articles.append(article)
                    if selected:
                        if f_tag.name in selected:
                            tag_list[f_tag.name]['articles'].append(article)
                    else:
                       tag_list[f_tag.name]['articles'].append(article)

                #import pdb;pdb.set_trace()


        #pprint(tag_list)

        return tag_list


    def get_context_data(self, **kwargs):
        c = {}
        data = super(TagListView, self).get_context_data(**kwargs)
        # import pdb;pdb.set_trace()

        qs = self.get_queryset()
        data.update({'object_list': qs})

        c.update(**data)
        return c"""