# Import necessary Django modules for creating views.
from django.views.generic import DetailView, ListView, RedirectView  # Provides base classes for common types of views.
from django.urls import reverse_lazy  # Used to generate URLs for redirecting.
from django.contrib import messages  # Allows us to display messages to the user.
from django.utils.translation import gettext_lazy as _  # Enables translation of text for multilingual support.
from django.shortcuts import redirect  # Simplifies URL redirection.

# Import the models that this view interacts with.
from polls.models import Choice, Poll, Vote
from django.http import JsonResponse  # Used to send JSON responses.

# This function handles the dynamic retrieval of choices for a given poll.
# It's typically called via AJAX when a user selects a poll, to display the choices for that poll.
def get_choices(request):
    # Get the poll ID from the query parameters in the URL.
    poll_id = request.GET.get('poll')
    # Fetch all choices that belong to the specified poll.
    choices = Choice.objects.filter(poll_id=poll_id)
    # Convert the choices into a list of dictionaries containing choice IDs and text.
    choices_list = [{'id': choice.id, 'text': choice.choice} for choice in choices]
    # Return the list of choices as a JSON response.
    return JsonResponse({'choices': choices_list})

# This view displays a list of all available polls.
# It uses a template to render the list and show the user the available polls.
class PollListView(ListView):
    model = Poll  # Specifies that this view displays data from the Poll model.
    template_name = 'polls/poll_list.html'  # Points to the template file that displays the list of polls.

# This view shows the details of a specific poll, including its question and choices.
class PollDetailView(DetailView):
    model = Poll  # Specifies that this view displays data from the Poll model.
    template_name = 'polls/poll_detail.html'  # Points to the template file that displays the poll's details.

    # This method adds additional data to the context that will be available in the template.
    def get_context_data(self, **kwargs):
        # Call the parent method to get the base context.
        context = super().get_context_data(**kwargs)
        poll = self.object  # The poll object being viewed.
        context['poll'] = poll
        # Determine if the user can vote (poll is active and the user hasn't already voted).
        context['poll'].votable = poll.can_vote(self.request.user)
        # Pass all choices for the poll to the template so they can be displayed.
        context['choices'] = poll.choice_set.all()
        return context

# This view handles the voting process for a poll.
# It redirects users back to the poll details page after they submit a vote.
class PollVoteView(RedirectView):
    # This method handles the logic when a user submits a vote.
    def post(self, request, *args, **kwargs):
        # Get the poll object based on the ID provided in the URL.
        poll = Poll.objects.get(id=kwargs['pk'])

        # Check if the poll is active; if not, display an error message and redirect back.
        if not poll.active:
            messages.error(request, _("This poll is inactive. You cannot vote."))
            return redirect('polls:detail', pk=poll.id)

        user = request.user  # Get the user who is submitting the vote.
        choice_id = request.POST.get('choice_pk')  # Get the selected choice ID from the form.

        # Check if a valid choice was selected.
        if choice_id:
            try:
                # Try to find the selected choice for the given poll.
                choice = Choice.objects.get(id=choice_id, poll=poll)
                # Create a new Vote record in the database.
                Vote.objects.create(poll=poll, user=user, choice=choice)
                messages.success(request, _("Thanks for your vote."))
            except Choice.DoesNotExist:
                # If the choice does not exist, show an error message.
                messages.error(request, _("Invalid choice."))
        else:
            # If no choice was selected, show an error message.
            messages.error(request, _("No choice was selected."))

        # Redirect the user back to the poll details page after submitting their vote.
        return super().post(request, *args, **kwargs)

    # This method defines the URL to redirect to after a vote is submitted.
    def get_redirect_url(self, **kwargs):
        # Redirect back to the detail view of the poll.
        return reverse_lazy('polls:detail', args=[kwargs['pk']])


