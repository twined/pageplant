from django.conf.urls import patterns, url

from pageplant.admin.views import (
    CreatePageView, ListPageView, UpdatePageView, DeletePageView,
    AddPageImageView, UploadPageImageView, ListPageImageView,
    RevertPageView,
    AJAXDeletePageImageView, CKEDITORBrowserView, ViewPageView,
    AJAXAutoCompleteTagsView
)

urlpatterns = patterns(
    'pageplant.admin.views',
    url(
        r'^$',
        ListPageView.as_view(),
        name="list"),
    url(
        r'^vis/(?P<pk>\d+)/$',
        ViewPageView.as_view(),
        name="view"),
    url(
        r'^ny/$',
        CreatePageView.as_view(),
        name="create"),
    url(
        r'^ny/autocomplete-tags/$',
        AJAXAutoCompleteTagsView.as_view(),
        name="autocomplete-tags"),
    url(
        r'^endre/(?P<pk>\d+)/$',
        UpdatePageView.as_view(),
        name="update"),
    url(
        r'^endre/(?P<pk>\d+)/autocomplete-tags/$',
        AJAXAutoCompleteTagsView.as_view(),
        name="autocomplete-tags"),
    url(
        r'^slett/(?P<pk>\d+)/$',
        DeletePageView.as_view(),
        name="delete"),
    url(
        r'^ny/check-slug/$',
        'checkslug',
        name="create-checkslug"),
    url(
        r'^endre/(?P<pk>\d+)/check-slug/$',
        'checkslug',
        name="edit-checkslug"),
    url(
        r'^endre/(?P<pk>\d+)/revert-to-revision/(?P<revision_id>\d+)$',
        RevertPageView.as_view(),
        name="edit-revert"),
    url(
        r'^(ny|endre)/get-keywords/$',
        'get_keywords',
        name="get-keywords"),
    url(
        r'^(ny|endre)/(.*)/get-keywords/$',
        'get_keywords',
        name="get-keywords"),

    # pageimages
    url(
        r'^imgs/browser/$',
        CKEDITORBrowserView.as_view(),
        name="browser"),
    url(
        r'^imgs/ny/$',
        AddPageImageView.as_view(),
        name="pageimage-create"),
    url(
        r'^imgs/ny/upload/$',
        UploadPageImageView.as_view(),
        name="pageimage-upload"),
    url(
        r'^imgs/oversikt/$',
        ListPageImageView.as_view(),
        name="pageimage-list"),
    url(
        r'^imgs/oversikt/slett/$',
        AJAXDeletePageImageView.as_view(),
        name="pageimage-delete"),
)
