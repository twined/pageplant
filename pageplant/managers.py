# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import models
from django.utils.translation import get_language

from .settings import PAGEPLANT_SETTINGS


class PublishedPagesManager(models.Manager):
    """
    Returns latest published pages
    """
    def get_queryset(self):
        qs = super(PublishedPagesManager, self).get_queryset()
        qs = qs.filter(status__exact=self.model.STATUS_PUBLISHED,
                       publish_at__lte=datetime.now())
        if PAGEPLANT_SETTINGS['multilanguage']:
            qs = qs.filter(language=get_language())

        return qs
