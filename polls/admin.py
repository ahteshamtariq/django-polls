from django.contrib import admin
from polls.models import Poll, Choice, Vote

# Inline choices for Poll in admin (allows adding choices directly in Poll form)
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1  # Shows one extra blank choice by default

# Admin config for Poll model
class PollAdmin(admin.ModelAdmin):
    model = Poll
    inlines = (ChoiceInline,)  # Attach choices inline
    list_display = ('question', 'count_choices', 'count_total_votes')  # Display these fields in the admin list view

# Admin config for Vote model
class VoteAdmin(admin.ModelAdmin):
    model = Vote
    list_display = ('choice', 'user', 'poll')  # Show choice, user, and poll in admin list view

    # Add custom JS for poll choice filtering in the admin
    class Media:
        js = ('polls/js/poll_choice_filter.js',)

# Register models in admin
admin.site.register(Poll, PollAdmin)
admin.site.register(Vote, VoteAdmin)
