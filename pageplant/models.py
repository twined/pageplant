# -*- coding: utf-8 -*-

"""
// PAGEPLANT
// model definitions for the pageplant app
// http://github.com/twined/pageplant
// (c) Twined/Univers 2009-2014. All rights reserved.
"""

from datetime import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models, transaction
from django.template.defaultfilters import slugify

import imgin.settings
from imgin.models import BaseImage

import reversion

from taggit.managers import TaggableManager

from .managers import PublishedPagesManager


class Page(models.Model):
    """
    Page model
    """
    PS_DRAFT = 0
    PS_WAITING = 1
    PS_PUBLISHED = 2
    PS_DELETED = 3

    PAGE_STATUS_TYPES = (
        (PS_DRAFT, 'Kladd'),
        (PS_WAITING, 'Venter'),
        (PS_PUBLISHED, 'Publisert'),
        (PS_DELETED, 'Slettet'),
    )

    language = models.CharField(max_length=10, blank=True)
    header = models.CharField(
        max_length=255, null=False, blank=False,
        verbose_name='Tittel')
    slug = models.CharField(max_length=255, verbose_name="URL", db_index=True)
    body = models.TextField(verbose_name="Brødtekst", blank=True)
    user = models.ForeignKey(User, verbose_name="Bruker")
    status = models.IntegerField(
        choices=PAGE_STATUS_TYPES, default=0, verbose_name='Status')
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Opprettet")
    updated = models.DateTimeField(auto_now=True, verbose_name="Endret")
    publish_at = models.DateTimeField(
        default=datetime.now, verbose_name='Publiseringstidspunkt')
    published = models.DateTimeField(
        null=True, blank=True, editable=False,
        verbose_name='Publisert', db_index=True)
    meta_keywords = models.CharField(
        max_length=255,
        null=True,
        verbose_name="Nøkkelord til søkemotorer")
    meta_description = models.CharField(
        max_length=255,
        null=True,
        verbose_name="Beskrivelse til søkemotorer")

    objects = models.Manager()
    published = PublishedPagesManager()
    tags = TaggableManager(blank=True)

    @property
    def status_class(self):
        """
        Returns post's current status for use as css class
        """
        return self.PAGE_STATUS_TYPES[self.status][1]
    '''
    def get_absolute_url(self):
        kwargs_dict = {
            "slug": self.slug,
            "year": self.created.year,
            "month": self.created.month,
            "day": self.created.day,
        }
        return reverse('pageplant:detail', kwargs=kwargs_dict)
    '''

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.header)
        super(Page, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.header

    class Meta:
        ordering = ('-created',)


def create_initial_revision(sender, **kwargs):
    if kwargs['raw']:
        return
    if kwargs['created']:
        page = kwargs['instance']
        with transaction.atomic(), reversion.create_revision():
            page.save()
            reversion.set_user(page.user)
            reversion.set_comment("Orginal versjon")

# connect signals
from django.db.models.signals import post_save, post_delete
from .cache import invalidate_cache
from actstream import action


def projects_action_handler_save(sender, instance, created, **kwargs):
    if kwargs['raw']:
        return
    if not created:
        action.send(instance.user, verb='endret', target=instance)
    else:
        action.send(instance.user, verb='opprettet', target=instance)

post_save.connect(
    projects_action_handler_save, sender=Page,
    dispatch_uid="Page.post_save.actstream"
)
post_save.connect(
    invalidate_cache, sender=Page,
    dispatch_uid="Page.post_save.invalidate"
)
post_save.connect(
    create_initial_revision, sender=Page,
    dispatch_uid="Page.post_save.create_initial_revision"
)
post_delete.connect(
    invalidate_cache, sender=Page,
    dispatch_uid="Page.post_delete.invalidate"
)

# register Page model as reversion object

reversion.register(Page)


class PageImage(BaseImage):
    """
    Models an image for upload and use through post object.
    Needs IMGIN
    """
    IMGIN_KEY = 'pageimage'
    IMGIN_CFG = imgin.settings.IMGIN_CONFIG[IMGIN_KEY]

    @staticmethod
    def get_create_url(*args, **kwargs):
        return reverse(
            'admin:pageplant:pageimage-create'
        )

    def get_delete_url():
        return reverse(
            'admin:pageplant:pageimage-delete'
        )

    @staticmethod
    def get_upload_url(*args, **kwargs):
        return reverse(
            'admin:pageplant:pageimage-upload'
        )

    @staticmethod
    def get_list_url(*args, **kwargs):
        return reverse(
            'admin:pageplant:pageimage-list'
        )

    class Meta:
        verbose_name = 'Sidebilde'
        verbose_name_plural = 'Sidebilder'

# connect signals
from django.db.models.signals import post_save, post_delete
from .cache import invalidate_cache
post_save.connect(
    invalidate_cache, sender=PageImage,
    dispatch_uid="PageImage.post_save.invalidate"
)
post_delete.connect(
    invalidate_cache, sender=PageImage,
    dispatch_uid="PageImage.post_delete.invalidate"
)
