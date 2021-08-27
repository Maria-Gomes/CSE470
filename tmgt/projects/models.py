from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Projects(models.Model):
    title = models.CharField(max_length=100)
    about = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    progress = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('projects-detail', kwargs={'pk': self.pk})

TASK_CHOICES = (("Complete", "Complete"),
                ("Incomplete", "Incomplete")
                )

class Tasks(models.Model):
    desc = models.TextField(max_length=100)
    deadline = models.DateField(null=True,blank=True)
    submit_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=10,choices=TASK_CHOICES, default="Incomplete")
    projects = models.ForeignKey(Projects, related_name='projects', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse('projects-detail', kwargs={'projects': self.projects})


# class WorkSpace(models.Model):
#     project = models.OneToOneField(Projects, on_delete=models.CASCADE)
#     members = models.ManyToManyField(User)
#
# class Comment(models.Model):
#     workspace = models.ForeignKey(WorkSpace, related_name="comment", on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     body = models.CharField(max_length=500)
#     date = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return '%s - %s' % (self.project.title, self.user)