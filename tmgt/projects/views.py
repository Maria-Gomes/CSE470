from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Projects
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)


# Create your views here.

def home(request):
    context = {
        'projects': Projects.objects.all()
    }
    return render(request, 'projects/home.html', context)

class ProjectsListView(ListView):
    model = Projects
    template_name = 'projects/home.html'
    context_object_name = 'projects'
    ordering = ['progress']

class ProjectsDetailView(DetailView):
    model = Projects

class ProjectsCreateView(LoginRequiredMixin, CreateView):
    model = Projects
    fields = ['title', 'about']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ProjectsUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Projects
    fields = ['title', 'about']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.author:
            return True
        return False

class ProjectsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Projects
    success_url = '/projects'

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.author:
            return True
        return False


# class TaskListView(ListView):
#     queryset = Tasks.objects.all().order_by(Tasks('deadline').desc(nulls_last=True))
#     template_name = 'projects/tasks.html'
#     context_object_name = 'tasks'