# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Please provide your full name', max_length=255)),
                ('email', models.EmailField(help_text=b'Please provide your valid email address', max_length=254)),
                ('body', models.TextField()),
            ],
        ),
    ]
