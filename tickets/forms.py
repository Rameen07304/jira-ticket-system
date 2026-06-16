
from django import forms
from .models import tickets

class TicketForm(forms.ModelForm):
    class Meta:
        model = tickets
        fields = ['status', 'priority']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].required = False
        self.fields['priority'].required = False
