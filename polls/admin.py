# This file customizes how the Poll, Choice, and Vote models appear in the Django admin panel.

from django.contrib import admin  # Importing Django's built-in admin tools.
from polls.models import Poll, Choice, Vote  # Importing our custom models from the polls app.

# This class allows us to add choices directly when we're adding or editing a poll in the admin.
# Think of it like being able to add ingredients (choices) while you're writing out a recipe (poll).
class ChoiceInline(admin.TabularInline):
    model = Choice  # Indicates that this inline is for the Choice model.
    extra = 1  # When adding a new poll, display 1 empty choice by default for easier data entry.

# This class customizes the admin page for Polls.
class PollAdmin(admin.ModelAdmin):
    model = Poll  # Specifies that this admin page is for the Poll model.
    inlines = (ChoiceInline,)  # Adds the ability to manage poll choices directly when viewing or editing a poll.
    
    # These fields will be shown in the table when listing all Polls in the admin.
    list_display = ('question', 'count_choices', 'count_total_votes', 'active')
    
    # Adds a filter on the right-hand side of the admin page to filter polls by their active status.
    # For example, you can quickly see only active or inactive polls.
    list_filter = ('active',)

# This class customizes the admin page for Votes.
# It controls how votes are added and ensures that admins can only pick valid choices.
class VoteAdmin(admin.ModelAdmin):
    model = Vote  # Specifies that this admin page is for the Vote model.
    list_display = ('choice', 'user', 'poll')  # These fields will show up when listing all votes.

    # This method customizes which choices are shown in the drop-down menu when adding or editing a vote.
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # If the field is "choice" and we're editing an existing vote...
        if db_field.name == "choice" and request._obj_:
            # ...show only the choices that belong to the selected poll.
            kwargs["queryset"] = Choice.objects.filter(poll=request._obj_.poll)
        # If the field is "poll", make sure that only active polls are shown in the dropdown.
        elif db_field.name == "poll":
            kwargs["queryset"] = Poll.objects.filter(active=True)
        # Call the original method with our updated query options.
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # This method stores the object being edited (a vote) for use in the above method.
    def get_form(self, request, obj=None, **kwargs):
        # Save the vote object we're editing, so we know which poll it's associated with.
        request._obj_ = obj
        return super().get_form(request, obj, **kwargs)

    # This part tells Django to include a specific JavaScript file on the vote admin page.
    # The JavaScript automatically updates the list of choices based on the selected poll.
    class Media:
        js = ('polls/js/poll_choice_filter.js',)

# Register our custom admin configurations for Polls and Votes so they appear in the admin panel.
admin.site.register(Poll, PollAdmin)
admin.site.register(Vote, VoteAdmin)



