from django.db import models
from django.utils import timezone
from datetime import date
from annoying.fields import AutoOneToOneField
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Entry(models.Model):
    title = models.CharField(max_length=30)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('entry-detail', kwargs={'pk': self.pk})
