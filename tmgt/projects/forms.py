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

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['desc'].label = "Description"
        self.fields['deadline'].label = "Deadline"
        self.fields['status'].label = "Status"
