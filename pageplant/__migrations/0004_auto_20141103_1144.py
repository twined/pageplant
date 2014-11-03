# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pageplant', '0003_auto_20141029_2143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='page',
            name='user',
        ),
        migrations.DeleteModel(
            name='Page',
        ),
        migrations.RemoveField(
            model_name='pageimage',
            name='user',
        ),
        migrations.DeleteModel(
            name='PageImage',
        ),
    ]
