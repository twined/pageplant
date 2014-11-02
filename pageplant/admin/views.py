# pages.py

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.shortcuts import redirect

from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import RedirectView
from django.views.generic import UpdateView

from cerebrum.mixins import LoginRequiredMixin
from cerebrum.mixins import DispatchProtectionMixin
from cerebrum.views import BaseAJAXCheckSlugView

from imgin.views import BaseImageCreateView
from imgin.views import AJAXBaseImageHandleUploadView
from imgin.views import AJAXBaseImageDeleteView
from imgin.views import BaseImageListView
from imgin.views import BaseAJAXFroalaBrowserView
from imgin.views import BaseAJAXFroalaUploadView

import reversion
from reversion.models import Version

from ..forms import PageForm
from ..models import Page
from ..models import PageImage


class AJAXCheckSlugView(BaseAJAXCheckSlugView):
    """
    Checks given slug against the database
    """
    model = Page


class RevertPageView(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        revision = Version.objects.get(pk=kwargs['revision_id'])
        revision.revision.revert()
        return reverse_lazy(
            'admin:pageplant:update', kwargs={'pk': kwargs['pk']})


class ListPageView(LoginRequiredMixin, ListView):
    model = Page
    context_object_name = "pages"
    template_name = "pageplant/admin/list.html"

    def get_queryset(self):
        return Page.objects.order_by('status', '-pk')


class ViewPageView(LoginRequiredMixin, DetailView):
    model = Page
    template_name = "pageplant/admin/detail.html"


class CreatePageView(DispatchProtectionMixin,
                     LoginRequiredMixin, CreateView):
    form_class = PageForm
    template_name = "pageplant/admin/form.html"
    success_url = reverse_lazy('admin:pageplant:list')

    def form_valid(self, form):
        with transaction.atomic(), reversion.create_revision():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            messages.success(self.request, "Siden er lagret.",
                             extra_tags='msg')
            reversion.set_user(self.request.user)
        return super(CreatePageView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Rett feilene under")
        return super(CreatePageView, self).form_invalid(form)


class UpdatePageView(DispatchProtectionMixin,
                     LoginRequiredMixin, UpdateView):
    model = Page
    form_class = PageForm
    template_name = "pageplant/admin/form.html"
    success_url = reverse_lazy('admin:pageplant:list')

    def form_valid(self, form):
        with transaction.atomic(), reversion.create_revision():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            messages.success(self.request, "Endringen var vellykket.",
                             extra_tags='msg')
            reversion.set_user(self.request.user)
            return super(UpdatePageView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Rett feilene under")
        return super(UpdatePageView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(UpdatePageView, self).get_context_data(**kwargs)
        context['body'] = self.object.body
        context['version_list'] = reversion.get_unique_for_object(self.object)
        context['editor_css'] = settings.PAGEPLANT_SETTINGS['editor_css']
        return context


class DeletePageView(LoginRequiredMixin, DeleteView):
    model = Page
    template_name = "pageplant/admin/delete.html"
    success_url = reverse_lazy('admin:pageplant:list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.get_success_url())


# -image----------------------------------------------------------------


class AJAXFroalaBrowserView(BaseAJAXFroalaBrowserView):
    model = PageImage


class AJAXFroalaUploadView(BaseAJAXFroalaUploadView):
    model = PageImage


class AddPageImageView(LoginRequiredMixin, BaseImageCreateView):
    model = PageImage


class ListPageImageView(LoginRequiredMixin, BaseImageListView):
    model = PageImage


class UploadPageImageView(LoginRequiredMixin,
                          AJAXBaseImageHandleUploadView):
    model = PageImage


class AJAXDeletePageImageView(LoginRequiredMixin,
                              AJAXBaseImageDeleteView):
    model = PageImage
