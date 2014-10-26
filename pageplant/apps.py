from django.apps import AppConfig
try:
    from actstream import registry
except ImportError:
    pass
else:

    class PageplantAppConfig(AppConfig):
        name = 'pageplant'

        def ready(self):
            registry.register(self.get_model('Page'))
