from django.conf.urls import patterns, url

from .views import PageDetailView

urlpatterns = patterns(
    '',
    url(r'^$',
        PageDetailView.as_view(), name='detail'),
)
