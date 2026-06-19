
from django import forms
from .models import tickets
class TicketForm(forms.ModelForm):
    class Meta:
        model = tickets
        fields = ['status', 'priority', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].required = False
        self.fields['priority'].required = False
        self.fields['due_date'].required = False

