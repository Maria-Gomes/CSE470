from django import forms
from django.forms import TimeInput

from .models import Entry

class EntryForm(forms.ModelForm):
    title = forms.CharField(label="Title", max_length=30)
    content = forms.CharField(label="Description",max_length=100)
    date = forms.DateField(required=True)

    class Meta:
        model = Entry
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        super(EntryForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Entry Title"
        self.fields['content'].label = "Description"