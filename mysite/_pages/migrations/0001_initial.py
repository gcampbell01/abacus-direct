# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import pages.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=500)),
                ('markup', models.CharField(default=b'restructuredtext', max_length=20, choices=[(b'restructuredtext', b'reStructuredText')])),
                ('slug', models.SlugField(unique=True)),
                ('content', models.TextField()),
                ('content_body', models.TextField(editable=False)),
                ('is_published', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('weight', models.IntegerField(help_text=b'The total count of page hits', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='EntryImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='A simple description about image.', max_length=100, blank=True)),
                ('image', models.ImageField(upload_to=b'radpress/entry_images/')),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
            },
            bases=(pages.models.ThumbnailModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveSmallIntegerField(default=3)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('entry_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pages.Entry')),
                ('cover_image', models.ForeignKey(to='pages.EntryImage', blank=True)),
            ],
            bases=('pages.entry',),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('entry_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pages.Entry')),
            ],
            bases=('pages.entry',),
        ),
        migrations.AddField(
            model_name='entry',
            name='tags',
            field=models.ManyToManyField(to='pages.Tag', blank=True),
        ),
        migrations.AddField(
            model_name='articletag',
            name='tag',
            field=models.ForeignKey(to='pages.Tag'),
        ),
        migrations.AddField(
            model_name='menu',
            name='page',
            field=models.ForeignKey(to='pages.Page'),
        ),
        migrations.AddField(
            model_name='articletag',
            name='article',
            field=models.ForeignKey(to='pages.Article'),
        ),
        migrations.AlterUniqueTogether(
            name='menu',
            unique_together=set([('order', 'page')]),
        ),
    ]
