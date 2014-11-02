from django.conf.urls import patterns, url

from cerebrum.views import AJAXGetKeywordsView
from cerebrum.views import AJAXAutoCompleteTagsView

from pageplant.admin.views import CreatePageView
from pageplant.admin.views import ListPageView
from pageplant.admin.views import UpdatePageView
from pageplant.admin.views import DeletePageView
from pageplant.admin.views import AddPageImageView
from pageplant.admin.views import UploadPageImageView
from pageplant.admin.views import ListPageImageView
from pageplant.admin.views import RevertPageView
from pageplant.admin.views import AJAXCheckSlugView
from pageplant.admin.views import AJAXDeletePageImageView
from pageplant.admin.views import ViewPageView
from pageplant.admin.views import AJAXFroalaBrowserView
from pageplant.admin.views import AJAXFroalaUploadView

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
        AJAXCheckSlugView.as_view(),
        name="create-checkslug"),
    url(
        r'^endre/(?P<pk>\d+)/check-slug/$',
        AJAXCheckSlugView.as_view(),
        name="edit-checkslug"),
    url(
        r'^endre/(?P<pk>\d+)/revert-to-revision/(?P<revision_id>\d+)$',
        RevertPageView.as_view(),
        name="edit-revert"),
    url(
        r'^(ny|endre)/get-keywords/$',
        AJAXGetKeywordsView.as_view(),
        name="get-keywords"),
    url(
        r'^(ny|endre)/(.*)/get-keywords/$',
        AJAXGetKeywordsView.as_view(),
        name="get-keywords"),

    # postimages
    # ----------
    # returns a json object of images to the froala browser
    url(
        r'^imgs/browser/$',
        AJAXFroalaBrowserView.as_view(),
        name="browser"),
    # uploads image to froala, returns the image as json
    url(
        r'^imgs/froala-upload/$',
        AJAXFroalaUploadView.as_view(),
        name="postimage-froala-upload"),
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
