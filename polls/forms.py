from django import forms
from polls.models import Choice, Vote

class VoteForm(forms.ModelForm):    
    choice = forms.MultipleChoiceField(
        choices=Choice.objects.none(),  # Queryset for the choices
        widget=forms.CheckboxSelectMultiple,  # Widget for multiple selection (Checkbox or Dropdown)
        required=True
    )

    class Meta:
        model = Vote
        fields = ['user','poll']
