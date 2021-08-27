from django.contrib import admin
from .models import Projects, Tasks, Comment
#, Comment, WorkSpace

# Register your models here.

admin.site.register(Projects)
admin.site.register(Tasks)
# admin.site.register(WorkSpace)
admin.site.register(Comment)
