# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import radpress.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
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
            ],
            options={
                'ordering': ('-created_at', '-updated_at'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ArticleTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('article', models.ForeignKey(to='radpress.Article')),
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
            bases=(radpress.models.ThumbnailModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveSmallIntegerField(default=3)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
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
            ],
            options={
                'ordering': ('-created_at', '-updated_at'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='page',
            name='tags',
            field=models.ManyToManyField(to='radpress.Tag', blank=True),
        ),
        migrations.AddField(
            model_name='menu',
            name='page',
            field=models.OneToOneField(to='radpress.Page'),
        ),
        migrations.AddField(
            model_name='articletag',
            name='tag',
            field=models.ForeignKey(to='radpress.Tag'),
        ),
        migrations.AddField(
            model_name='article',
            name='cover_image',
            field=models.ForeignKey(blank=True, to='radpress.EntryImage', null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='radpress.Tag', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='menu',
            unique_together=set([('order', 'page')]),
        ),
    ]
