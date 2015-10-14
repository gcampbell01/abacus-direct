# Auto Generated with make_admin
# ######################################################## #
# YOU MUST DELETE THE ABOVE STATEMENT                      #
# IF YOU DO NOT WANT ./manage.py change_model <model_name> #
# TO REGENERATE THIS admin.py                              #
# YOUR CHANGES WILL BE OVERWRITTEN                         #
############################################################

from django.contrib import admin
from models import Tag, EntryImage, Entry, Article, ArticleTag, Page, Menu

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', )
    list_filter = ('name', 'slug', )
    search_fields = ('name', 'slug', )
    #fields = ('name', 'slug', )
    filter_horizontal = ()
    #exclude = (,)

class EntryImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', )
    list_filter = ('name', 'image', )
    search_fields = ('name', 'image', )
    #fields = ('name', 'image', )
    filter_horizontal = ()
    #exclude = (,)

class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'markup', 'slug', 'content', 'content_body', 'is_published', 'created_at', 'updated_at', 'weight', )
    list_filter = ('title', 'markup', 'slug', 'content', 'content_body', 'is_published', 'created_at', 'updated_at', 'weight', )
    search_fields = ('title', 'markup', 'slug', 'content', 'content_body', 'is_published', 'created_at', 'updated_at', 'weight', )
    #fields = ('title', 'markup', 'slug', 'content', 'content_body', 'is_published', 'created_at', 'updated_at', 'weight', )
    filter_horizontal = ()
    #exclude = (,)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'markup', 'slug', 'content', 'content_body', 'is_published', 'created_at', 'updated_at', 'weight', 'entry_ptr', 'cover_image', )
    list_filter = ('title', 'markup', 'slug', 'content', 'content_body', 'is_published', 'created_at', 'updated_at', 'weight', 'entry_ptr', 'cover_image', )
    search_fields = ('title', 'markup', 'slug', 'content', 'content_body', 'is_published', 'created_at', 'updated_at', 'weight', 'entry_ptr', 'cover_image', )
    #fields = ('title', 'markup', 'slug', 'content', 'content_body', 'is_published', 'created_at', 'updated_at', 'weight', 'entry_ptr', 'cover_image', )
    filter_horizontal = ()
    #exclude = (,)

class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ('tag', 'article', )
    list_filter = ('tag', 'article', )
    search_fields = ('tag', 'article', )
    #fields = ('tag', 'article', )
    filter_horizontal = ()
    #exclude = (,)

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'markup', 'slug', 'content', 'content_body', 'is_published', 'created_at', 'updated_at', 'weight', 'entry_ptr', )
    list_filter = ('title', 'markup', 'slug', 'content', 'content_body', 'is_published', 'created_at', 'updated_at', 'weight', 'entry_ptr', )
    search_fields = ('title', 'markup', 'slug', 'content', 'content_body', 'is_published', 'created_at', 'updated_at', 'weight', 'entry_ptr', )
    #fields = ('title', 'markup', 'slug', 'content', 'content_body', 'is_published', 'created_at', 'updated_at', 'weight', 'entry_ptr', )
    filter_horizontal = ()
    #exclude = (,)

class MenuAdmin(admin.ModelAdmin):
    list_display = ('order', 'page', )
    list_filter = ('order', 'page', )
    search_fields = ('order', 'page', )
    #fields = ('order', 'page', )
    filter_horizontal = ()
    #exclude = (,)



admin.site.register(Tag, TagAdmin)
admin.site.register(EntryImage, EntryImageAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleTag, ArticleTagAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Menu, MenuAdmin)

