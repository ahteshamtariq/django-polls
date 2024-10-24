from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from polls.views import PollDetailView, PollListView, PollVoteView, get_choices

# URL patterns for the polls app
urlpatterns = [
    path('', PollListView.as_view(), name='list'),  # List all polls
    re_path(r'^(?P<pk>\d+)/$', PollDetailView.as_view(), name='detail'),  # Poll detail view by ID
    re_path(r'^(?P<pk>\d+)/vote/$', login_required(PollVoteView.as_view()), name='vote'),  # Vote on a poll (login required)
    path('get_choices/', get_choices, name='get_choices'),  # Fetch poll choices (AJAX or similar)
]
