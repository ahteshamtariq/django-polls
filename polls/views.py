from django.views.generic import DetailView, ListView, RedirectView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from polls.models import Choice, Poll, Vote
from django.http import JsonResponse

# Return choices for a poll as JSON
def get_choices(request):
    poll_id = request.GET.get('poll')
    choices = Choice.objects.filter(poll_id=poll_id)
    choices_list = [{'id': choice.id, 'text': choice.choice} for choice in choices]
    return JsonResponse({'choices': choices_list})


# List all polls
class PollListView(ListView):
    model = Poll


# Show details of a specific poll
class PollDetailView(DetailView):
    model = Poll

    # Add votable status for the poll
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['poll'].votable = self.object.can_vote(self.request.user)
        return context


# Handle poll voting and redirect
class PollVoteView(RedirectView):
    def post(self, request, *args, **kwargs):
        # Get the poll being voted on
        poll = Poll.objects.get(id=kwargs['pk'])
        user = request.user
        # Get the selected choice
        choice = Choice.objects.get(id=request.POST['choice_pk'])
        Vote.objects.create(poll=poll, user=user, choice=choice)
        messages.success(request, _("Thanks for your vote."))
        return super().post(request, *args, **kwargs)

    # Redirect the user to the poll's detail page after voting
    def get_redirect_url(self, **kwargs):
        return reverse_lazy('polls:detail', args=[kwargs['pk']])
