# pages.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.db import transaction
from django.shortcuts import redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import (
    CreateView, ListView, UpdateView,
    DeleteView, DetailView, View,
    RedirectView
)

from taggit.models import Tag
from cerebrum.views import LoginRequiredMixin
from cerebrum.utils import json_response
from imgin.views import (
    BaseImageCreateView, AJAXBaseImageHandleUploadView,
    AJAXBaseImageDeleteView, BaseImageListView, BaseCKEDITORBrowserView
)

import reversion

from ..models import Page, PageImage
from ..forms import PageForm


@login_required
def get_keywords(request, *args, **kwargs):
    keywords = request.GET['text']
    return json_response({
        'keywords': keywords,
    })

@login_required
def checkslug(request, pk=None, *args, **kwargs):
    if not 'slug' in request.GET:
        # slug wasn't passed.
        return json_response({
            'status': 400,
            'error_msg': 'No slug passed to pages::checkslug'
        })

    slug = request.GET['slug'].lower()

    if pk:
        # it's an edit. it's ok if it's the same as before
        page = Page.objects.get(pk=pk)
        if page.slug == slug:
            return json_response({
                'status': 200,
            })

    if Page.objects.all().filter(slug=slug):
        return json_response({
            'status': 300,
            'error_msg': 'Overskriften eksisterer allerede'
        })

    return json_response({
        'status': 200,
    })

from reversion.models import Version


class RevertPageView(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        revision = Version.objects.get(pk=kwargs['revision_id'])
        revision.revision.revert()
        return reverse_lazy('admin:pageplant:update', kwargs={'pk': kwargs['pk']})


class ListPageView(LoginRequiredMixin, ListView):
    model = Page
    context_object_name = "pages"
    template_name = "pageplant/admin/list.html"

    def get_queryset(self):
        return Page.objects.order_by('status', '-pk')


class ViewPageView(LoginRequiredMixin, DetailView):
    model = Page
    template_name = "pageplant/admin/detail.html"


class CreatePageView(LoginRequiredMixin, CreateView):
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


class UpdatePageView(LoginRequiredMixin, UpdateView):
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
        return context


class DeletePageView(LoginRequiredMixin, DeleteView):
    model = Page
    template_name = "pageplant/admin/page_confirm_delete.html"
    success_url = reverse_lazy('admin:pageplant:list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.get_success_url())


class AJAXAutoCompleteTagsView(View):
    """
    AJAX: Returns tags
    """
    def get(self, request, *args, **kwargs):
        try:
            tags = Tag.objects.filter(name__istartswith=request.GET['query']).values_list('name', flat=True)
        except MultiValueDictKeyError:
            tags = []

        return json_response({'suggestions': list(tags)})

# -image----------------------------------------------------------------


class CKEDITORBrowserView(BaseCKEDITORBrowserView):
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
