# Import necessary Django modules for URL routing.
from django.urls import path, re_path  # 'path' and 're_path' are used to define URL patterns.
from django.contrib.auth.decorators import login_required  # Ensures that certain views are accessible only to logged-in users.

# Import views that will handle the behavior for each URL.
from polls.views import PollDetailView, PollListView, PollVoteView, get_choices

# Define URL patterns for the 'polls' app.
urlpatterns = [
    # The empty string ('') means that this is the homepage of the 'polls' app.
    # When a user visits the base URL for 'polls/', this pattern will match.
    # It will display a list of polls using the PollListView.
    path('', PollListView.as_view(), name='list'),

    # This pattern matches URLs like 'polls/5/', where '5' is the ID of the poll.
    # The 'pk' parameter captures the poll's primary key (ID) from the URL.
    # It will display the details of a specific poll using the PollDetailView.
    re_path(r'^(?P<pk>\d+)/$', PollDetailView.as_view(), name='detail'),

    # This pattern matches URLs like 'polls/5/vote/', where '5' is the ID of the poll.
    # The 'login_required' decorator ensures that only logged-in users can access this view.
    # It allows users to cast their vote on a poll using the PollVoteView.
    re_path(r'^(?P<pk>\d+)/vote/$', login_required(PollVoteView.as_view()), name='vote'),

    # This pattern handles the 'polls/get_choices/' URL.
    # It is used to dynamically retrieve the choices for a specific poll, often through AJAX requests.
    # This is typically called when a poll is selected, so that the user sees only relevant choices.
    path('get_choices/', get_choices, name='get_choices'),
]
