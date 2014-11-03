# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pageplant', '0002_auto_20141024_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='slug',
            field=models.CharField(max_length=255, verbose_name=b'URL', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pageimage',
            name='image',
            field=models.ImageField(upload_to=b'images'),
            preserve_default=True,
        ),
    ]
