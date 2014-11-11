# pages.py

from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.shortcuts import redirect

from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import RedirectView
from django.views.generic import UpdateView

from cerebrum.mixins import DispatchProtectionMixin
from cerebrum.mixins import FormMessagesMixin
from cerebrum.mixins import LoginRequiredMixin

from imgin.views import BaseImageCreateView
from imgin.views import AJAXBaseImageHandleUploadView
from imgin.views import AJAXBaseImageDeleteView
from imgin.views import BaseImageListView

import reversion
from reversion.models import Version

from ..forms import BasePageForm
from ..models import BasePage
from ..models import BaseTreePage
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


class BaseListTreePageView(LoginRequiredMixin, ListView):
    model = BaseTreePage
    context_object_name = "pages"
    template_name = "pageplant/admin/list_tree.html"

    def get_queryset(self):
        return self.model.objects.filter(level=0).\
            order_by('-is_partial', 'status', '-pk')


class BaseViewPageView(LoginRequiredMixin, DetailView):
    model = BasePage
    template_name = "pageplant/admin/detail.html"

    def get_context_data(self, **kwargs):
        context = super(BaseViewPageView, self).get_context_data(**kwargs)
        context['editor_css'] = settings.PAGEPLANT_SETTINGS['editor_css']
        return context


class BaseCreatePageView(FormMessagesMixin,
                         DispatchProtectionMixin,
                         LoginRequiredMixin,
                         CreateView):

    form_class = BasePageForm
    form_valid_message = "Siden er lagret"
    form_invalid_message = "Rett feilene under"
    template_name = "pageplant/admin/form.html"
    success_url = reverse_lazy('admin:pages:list')

    def form_valid(self, form):
        with transaction.atomic(), reversion.create_revision():
            form.instance.user = self.request.user
            reversion.set_user(self.request.user)
            ret = super(BaseCreatePageView, self).form_valid(form)
            return ret

    def get_context_data(self, **kwargs):
        context = super(BaseCreatePageView, self).get_context_data(**kwargs)
        context['editor_css'] = settings.PAGEPLANT_SETTINGS['editor_css']
        return context


class BaseUpdatePageView(FormMessagesMixin,
                         DispatchProtectionMixin,
                         LoginRequiredMixin,
                         UpdateView):

    model = BasePage
    form_class = BasePageForm
    form_valid_message = "Siden er oppdatert"
    form_invalid_message = "Rett feilene under"
    template_name = "pageplant/admin/form.html"
    success_url = reverse_lazy('admin:pages:list')

    def form_valid(self, form):
        with transaction.atomic(), reversion.create_revision():
            form.instance.user = self.request.user
            reversion.set_user(self.request.user)
            ret = super(BaseUpdatePageView, self).form_valid(form)
            return ret

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
