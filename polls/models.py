# Import necessary Django modules for working with models and settings.
from django.conf import settings  # Allows us to reference Django's user model.
from django.db import models  # Provides tools for defining database models.

# This model represents a Poll, which is a question that users can vote on.
class Poll(models.Model):
    # 'question' is the main text of the poll, limited to 255 characters.
    question = models.CharField(max_length=255)

    # 'description' provides more details about the poll, and it can be left empty.
    description = models.TextField(blank=True)

    # 'active' indicates if the poll is currently open for voting.
    # For example, a closed poll would not allow users to vote.
    active = models.BooleanField(default=True)  # Default is 'True', meaning the poll is open when created.

    # Returns the total number of choices available for this poll.
    def count_choices(self):
        # Accesses related 'Choice' objects through Django's automatic reverse relationship.
        return self.choice_set.count()

    # Returns the total number of votes across all choices for this poll.
    def count_total_votes(self):
        result = 0
        # Loops through each choice related to this poll and sums their votes.
        for choice in self.choice_set.all():
            result += choice.count_votes()
        return result

    # Checks if a user can vote on this poll.
    # A user can only vote if the poll is active and they haven't voted yet.
    def can_vote(self, user):
        return self.active and not self.vote_set.filter(user=user).exists()

    # Defines how the poll is displayed as text, useful in the admin panel.
    def __str__(self):
        return self.question

# This model represents a Choice, which is one of the possible answers to a Poll.
class Choice(models.Model):
    # Each choice is linked to a specific poll.
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    # 'choice' is the text of the answer option, limited to 255 characters.
    choice = models.CharField(max_length=255)

    # Returns the number of votes this choice has received.
    def count_votes(self):
        return self.vote_set.count()

    # Defines how the choice is displayed as text, useful in the admin panel.
    def __str__(self):
        return self.choice

    # Orders the choices alphabetically or as specified.
    class Meta:
        ordering = ['choice']  # Choices will appear in alphabetical order in lists.

# This model represents a Vote, which ties a user to a choice they selected for a poll.
class Vote(models.Model):
    # Each vote is tied to a specific user, who cast the vote.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Each vote is tied to a specific poll.
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    # Each vote is tied to a specific choice within that poll.
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    # Defines how the vote is displayed as text, useful in the admin panel.
    def __str__(self):
        return f'Vote for {self.choice}'

    # Ensures that each user can vote only once per poll.
    class Meta:
        unique_together = (('user', 'poll'),)  # Prevents duplicate votes from the same user on a single poll.




