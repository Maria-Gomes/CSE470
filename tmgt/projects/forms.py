from django import forms
from .models import Tasks, Comment

TASK_CHOICES = (("Complete", "Complete"),
                ("Incomplete", "Incomplete")
                )

class TaskForm(forms.ModelForm):
    desc = forms.CharField(label="Description",max_length=100)
    deadline = forms.DateField(required=False)
    status = forms.ChoiceField(choices=TASK_CHOICES)

    class Meta:
        model = Tasks
        fields = ['desc', 'deadline', 'status', 'submit_time']

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['desc'].label = "Description"
        self.fields['deadline'].label = "Submission Date"
        self.fields['submit_time'].label = "Submission Time"
        self.fields['status'].label = "Status"


class CommentForm(forms.ModelForm):
    body = forms.CharField(max_length=500)

    class Meta:
        model = Comment
        fields = ['body']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].label = "Write a Comment"
