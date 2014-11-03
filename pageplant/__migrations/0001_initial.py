# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields
import datetime
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(max_length=10, blank=True)),
                ('header', models.CharField(max_length=255, verbose_name=b'Overskrift')),
                ('slug', models.CharField(max_length=255, verbose_name=b'URL')),
                ('body', models.TextField(verbose_name=b'Br\xc3\xb8dtekst', blank=True)),
                ('status', models.IntegerField(default=0, verbose_name=b'Status', choices=[(0, b'Kladd'), (1, b'Venter'), (2, b'Publisert'), (3, b'Slettet')])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'Opprettet')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name=b'Endret')),
                ('publish_at', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Publiseringstidspunkt')),
                ('meta_keywords', models.CharField(max_length=255, null=True, verbose_name=b'N\xc3\xb8kkelord til s\xc3\xb8kemotorer')),
                ('meta_description', models.CharField(max_length=255, null=True, verbose_name=b'Beskrivelse til s\xc3\xb8kemotorer')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags')),
                ('user', models.ForeignKey(verbose_name=b'Bruker', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', sorl.thumbnail.fields.ImageField(upload_to=b'images')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField()),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Sidebilde',
                'verbose_name_plural': 'Sidebilder',
            },
            bases=(models.Model,),
        ),
    ]
