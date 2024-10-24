from django.conf import settings
from django.db import models
# from django.utils.encoding import python_2_unicode_compatible  # No longer needed in modern Django.

# Poll model, for questions in the poll
class Poll(models.Model):
    question = models.CharField(max_length=255)
    description = models.TextField(blank=True)  # Optional description

    # Count how many choices a poll has
    def count_choices(self):
        return self.choice_set.count()

    # Sum up all votes for this poll
    def count_total_votes(self):
        result = 0
        for choice in self.choice_set.all():
            result += choice.count_votes()
        return result

    # Check if a user can still vote
    def can_vote(self, user):
        return not self.vote_set.filter(user=user).exists()

    # String representation: return the poll question
    def __str__(self):
        return self.question


# Choices linked to a poll
class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)  # Links choice to a poll
    choice = models.CharField(max_length=255)  # Choice text

    # Count votes for this choice
    def count_votes(self):
        return self.vote_set.count()

    # String representation: return choice text
    def __str__(self):
        return self.choice

    # Sort choices alphabetically
    class Meta:
        ordering = ['choice']


# Votes linked to a user, poll, and choice
class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # The user voting
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)  # The poll they're voting in
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)  # The choice they picked

    # String representation: show which choice was voted for
    def __str__(self):
        return u'Vote for %s' % (self.choice)

    # Ensure a user can only vote once per poll
    class Meta:
        unique_together = (('user', 'poll'))
