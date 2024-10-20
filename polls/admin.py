from django.contrib import admin

from polls.models import Poll, Choice, Vote


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class PollAdmin(admin.ModelAdmin):
    model = Poll
    inlines = (ChoiceInline,)
    list_display = ('question', 'count_choices', 'count_total_votes')


class VoteAdmin(admin.ModelAdmin):
    model = Vote
    list_display = ('choice', 'user', 'poll')

    class Media:
        js = ('polls/js/poll_choice_filter.js',)

admin.site.register(Poll, PollAdmin)
admin.site.register(Vote, VoteAdmin)
