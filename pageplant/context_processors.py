# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Context processors for the Pageplant app
# Provides {{ admin }} dictionary in all templates.
# (c) Twined/Univers 2009-2014. All rights reserved.
# ----------------------------------------------------------------------

import datetime

from .settings import PAGEPLANT_SETTINGS


def config(request):
    cfg = PAGEPLANT_SETTINGS
    return {'pageplant_settings': cfg}


def date_now(request):
    return {'date_now': datetime.datetime.now()}
