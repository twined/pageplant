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

from imgin.views import BaseImageCreateView
from imgin.views import AJAXBaseImageHandleUploadView
from imgin.views import AJAXBaseImageDeleteView
from imgin.views import BaseImageListView

import reversion
from reversion.models import Version

from ..forms import BasePageForm
from ..models import BasePage
from ..models import BasePageImage


class BaseRevertPageView(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        revision = Version.objects.get(pk=kwargs['revision_id'])
        revision.revision.revert()
        return reverse_lazy(
            'admin:pages:update', kwargs={'pk': kwargs['pk']})


class BaseListPageView(LoginRequiredMixin, ListView):
    model = BasePage
    context_object_name = "pages"
    template_name = "pageplant/admin/list.html"

    def get_queryset(self):
        return self.model.objects.order_by('-is_partial', 'status', '-pk')


class BaseViewPageView(LoginRequiredMixin, DetailView):
    model = BasePage
    template_name = "pageplant/admin/detail.html"


class BaseCreatePageView(DispatchProtectionMixin,
                         LoginRequiredMixin, CreateView):
    form_class = BasePageForm
    template_name = "pageplant/admin/form.html"
    success_url = reverse_lazy('admin:pages:list')

    def form_valid(self, form):
        with transaction.atomic(), reversion.create_revision():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            messages.success(self.request, "Siden er lagret.",
                             extra_tags='msg')
            reversion.set_user(self.request.user)
        return super(BaseCreatePageView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Rett feilene under")
        return super(BaseCreatePageView, self).form_invalid(form)


class BaseUpdatePageView(DispatchProtectionMixin,
                         LoginRequiredMixin, UpdateView):
    model = BasePage
    form_class = BasePageForm
    template_name = "pageplant/admin/form.html"
    success_url = reverse_lazy('admin:pages:list')

    def form_valid(self, form):
        with transaction.atomic(), reversion.create_revision():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            messages.success(self.request, "Endringen var vellykket.",
                             extra_tags='msg')
            reversion.set_user(self.request.user)
            return super(BaseUpdatePageView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Rett feilene under")
        return super(BaseUpdatePageView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(BaseUpdatePageView, self).get_context_data(**kwargs)
        context['body'] = self.object.body
        context['version_list'] = reversion.get_unique_for_object(self.object)
        context['editor_css'] = settings.PAGEPLANT_SETTINGS['editor_css']
        return context


class BaseDeletePageView(LoginRequiredMixin, DeleteView):
    model = BasePage
    template_name = "pageplant/admin/delete.html"
    success_url = reverse_lazy('admin:pages:list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.get_success_url())


class BaseAddPageImageView(LoginRequiredMixin, BaseImageCreateView):
    model = BasePageImage


class BaseListPageImageView(LoginRequiredMixin, BaseImageListView):
    model = BasePageImage


class BaseUploadPageImageView(LoginRequiredMixin,
                              AJAXBaseImageHandleUploadView):
    model = BasePageImage


class BaseAJAXDeletePageImageView(LoginRequiredMixin,
                                  AJAXBaseImageDeleteView):
    model = BasePageImage
