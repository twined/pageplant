# -*- coding: utf-8 -*-
from django.views.generic import DetailView

from .models import BasePage
from .settings import PAGEPLANT_SETTINGS


class BasePageDetailView(DetailView):
    model = BasePage
    context_object_name = "page"
    template_name = "pageplant/detail.html"

    def get_queryset(self):
        return self.model.published.all().filter(
            slug__iexact=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(BasePageDetailView, self).get_context_data(**kwargs)
        context['title_prefix'] = PAGEPLANT_SETTINGS['title_prefix']
        return context
