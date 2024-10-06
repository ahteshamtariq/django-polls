from django.urls import path, re_path
from django.contrib.auth.decorators import login_required

from polls.views import PollDetailView, PollListView, PollVoteView

urlpatterns = [
    path('', PollListView.as_view(), name='list'),
    re_path(r'^(?P<pk>\d+)/$', PollDetailView.as_view(), name='detail'),
    re_path(r'^(?P<pk>\d+)/vote/$', login_required(PollVoteView.as_view()), name='vote'),
]