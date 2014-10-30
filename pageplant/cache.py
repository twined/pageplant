from cerebrum.cache import cache_delete_pattern


def invalidate_cache(sender, **kwargs):
    """
    Invalidates all views using Page object
    """
    cache_delete_pattern('pageplant.*')
