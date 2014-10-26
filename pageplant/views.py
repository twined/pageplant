# -*- coding: utf-8 -*-
from django.views.generic import DetailView

from hiver.views import CacheMixin

from .models import Page
from .settings import PAGEPLANT_SETTINGS


class PageDetailView(CacheMixin, DetailView):
    model = Page
    context_object_name = "page"
    template_name = "pageplant/detail.html"
    cache_path = "pageplant.view"

    def get_queryset(self):
        return Page.published.all().filter(
            slug__iexact=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(PageDetailView, self).get_context_data(**kwargs)
        context['title_prefix'] = PAGEPLANT_SETTINGS['title_prefix']
        return context
