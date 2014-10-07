PAGEPLANT
=========

**NOTE: This is tailored for the twined project structure,
it probably won't work too well without customization on other
project bootstraps.**

Installation:
-------------

    pip install -e git://github.com/twined/pageplant.git#egg=pageplant-dev


Usage:
------

Add `pageplant` to `INSTALLED_APPS` and add this to the end
of your urlpatterns:

    # urls
    url(
        r'^(?P<slug>[-\w]+)/$', include('pageplant.urls', namespace="pageplant")
    ),

Then add this to your `settings.py`

    # default pageplant settings

    PAGEPLANT_SETTINGS = {
        'multilanguage': False,
        'default_language': 'en',
        'languages': (('en', 'English'),),
    }

Remember to add a `pageimage` key to the IMGIN_CONFIG in your `settings.py`:

    # example IMGIN config

    IMGIN_CONFIG = {
        # ...
        'pageimage': {
            'allowed_exts': [".jpg", ".png", ".jpeg",
                             ".JPG", ".PNG", ".JPEG"],
            'upload_dir': os.path.join('images', 'pages'),
            'size_limit': 10240000,
            'size_map': {
                'l': {
                    'landscape': '700',
                    'portrait': '700',
                    'dir': 'l',
                    'class_name': 'large',
                    'crop': '',
                    'quality': 90,
                    'format': 'JPEG',
                },
                'm': {
                    'landscape': '310',
                    'portrait': '310',
                    'dir': 'm',
                    'class_name': 'medium',
                    'crop': '',
                    'quality': 90,
                    'format': 'JPEG',
                },
                's': {
                    'landscape': '200',
                    'portrait': '200',
                    'dir': 's',
                    'class_name': 'small',
                    'crop': '',
                    'quality': 90,
                    'format': 'JPEG',
                },
                't': {
                    'landscape': '140x140',
                    'portrait': '140x140',
                    'dir': 't',
                    'class_name': 'thumb',
                    'crop': 'center',
                    'quality': 90,
                    'format': 'JPEG',
                },
            },
        },
    }

Overridable templates:

    /pageplant/detail.html

Object name is `pages` and `page`.
