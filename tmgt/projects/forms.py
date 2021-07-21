from django import forms
from .models import Tasks

TASK_CHOICES = (("Complete", "Complete"),
                ("Incomplete", "Incomplete")
                )

class TaskForm(forms.ModelForm):
    desc = forms.CharField(label="Description",max_length=100)
    deadline = forms.DateField(required=False)
    status = forms.ChoiceField(choices=TASK_CHOICES)

    class Meta:
        model = Tasks
        fields = ['desc', 'deadline', 'status']
