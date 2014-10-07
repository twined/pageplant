from django.core.cache import cache


def invalidate_cache(sender, **kwargs):
    """
    Invalidates all views using Page object
    """
    cache.delete_pattern('pageplant.*')
