from django.conf import settings

PAGEPLANT_SETTINGS = {
    'title_prefix': '',
    'multilanguage': False,
    'default_language': 'en',
    'languages': (('en', 'English'),),
}

PAGEPLANT_SETTINGS.update(getattr(settings, 'PAGEPLANT_SETTINGS', {}))
