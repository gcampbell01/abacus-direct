# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='sender',
            field=models.EmailField(default=b'email@example.com', help_text=b'Please provide your valid email address', max_length=254),
        ),
        migrations.AddField(
            model_name='email',
            name='subject',
            field=models.CharField(help_text=b'Please provide an email subject', max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='email',
            field=models.EmailField(help_text=b'Please provide the email address to send to', max_length=254),
        ),
    ]
