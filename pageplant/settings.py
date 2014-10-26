from django.conf import settings

PAGEPLANT_SETTINGS = {
    'title_prefix': '',
    'multilanguage': False,
    'default_language': 'en',
    'languages': (('en', 'English'),),
    'editor_css': 'admin/css/pageplant-editor.css',
    'url_base': 'pageplant',
    'namespace': 'pageplant',
}

PAGEPLANT_SETTINGS.update(getattr(settings, 'PAGEPLANT_SETTINGS', {}))
