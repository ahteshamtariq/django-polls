from django.conf import settings
from django.db import models
# from django.utils.encoding import python_2_unicode_compatible


# @python_2_unicode_compatible
class Poll(models.Model):
    question = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def count_choices(self):
        return self.choice_set.count()

    def count_total_votes(self):
        result = 0
        for choice in self.choice_set.all():
            result += choice.count_votes()
        return result

    def can_vote(self, user):
        return not self.vote_set.filter(user=user).exists()

    def __str__(self):
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.CharField(max_length=255)

    def count_votes(self):
        return self.vote_set.count()

    def __str__(self):
        return self.choice

    class Meta:
        ordering = ['choice']


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return u'Vote for %s' % (self.choice)

    class Meta:
        unique_together = (('user', 'poll'))
