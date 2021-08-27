from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from projects.models import Tasks

from django.urls import reverse

# Create your models here.
class Event(models.Model):
    e_user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    desc = models.TextField(max_length=100)
    date = models.DateField()
    start_t = models.TimeField(null=True, blank=True)
    end_t = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.pk})