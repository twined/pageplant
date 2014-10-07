from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse_lazy
from .models import Page


class PagesListSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return [reverse_lazy('pageplant:list')]

    def location(self, obj):
        return obj

    def lastmod(self, obj):
        page = Page.published.all().order_by('-updated')[:1]
        if page:
            return page[0].updated


class PageDetailSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Page.published.all()

    def lastmod(self, obj):
        return obj.updated
