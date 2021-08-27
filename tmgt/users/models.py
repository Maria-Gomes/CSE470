from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from projects.models import Tasks
from cal.models import Event

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.user.username} Profile'

class Notification(models.Model):
    #1.Task Deadline 2.Event 3.Comment
    notif_type = models.IntegerField()
    to_user = models.ForeignKey(User, related_name= "notif_to", on_delete=models.CASCADE)
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    notif_seen = models.BooleanField(default=False)