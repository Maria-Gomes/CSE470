from django import forms
from django.forms import TimeInput

from .models import Event

class EventForm(forms.ModelForm):
    name = forms.CharField(label="Title", max_length=30)
    desc = forms.CharField(label="Description",max_length=100)
    date = forms.DateField(required=True)
    start_t = forms.TimeField(required=False)
    end_t = forms.TimeField(required=False)

    class Meta:
        model = Event
        fields = ['name', 'desc', 'date', 'start_t', 'end_t']

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Event Title"
        self.fields['desc'].label = "Description"
        self.fields['date'].label = "Scheduled Date"
        self.fields['start_t'].label = "Start Time"
        self.fields['end_t'].label = "End Time"