from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import Projects, Tasks
from .forms import TaskForm
from django.db.models import F
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)


# Create your views here.


class ProjectsListView(ListView):
    model = Projects
    template_name = 'projects/home.html'
    context_object_name = 'projects'
    ordering = ['progress']

class ProjectsDetailView(DetailView):
    model = Projects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Tasks.objects.filter(projects=self.object)
        context['t_form'] = TaskForm()
        return context


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

class TasksUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Tasks
    fields = ['desc', 'deadline', 'status']

    def form_valid(self, t_form):
        t_form.instance.user = self.request.user
        return super().form_valid(t_form)

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['t_form'] = TaskForm(instance=self.get_object())
        return context

    def get_success_url(self):
        projects = self.object.projects
        return reverse_lazy('projects-detail', args=(projects.id,))


class TasksDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tasks
    context_object_name = 'task'

    def get_success_url(self):
        projects = self.object.projects
        return reverse_lazy('projects-detail', args=(projects.id,))

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.user:
            return True
        return False

def home(request):
    context = {
        'projects': Projects.objects.all()
    }
    return render(request, 'projects/home.html', context)

@login_required(login_url='/')
def addTask(request, pk):

    if request.method == 'POST':
        t_form = TaskForm(request.POST)
        if t_form.is_valid():
            task = t_form.save(commit=False)
            task.user = request.user
            task.projects = Projects.objects.get(pk=pk)
            task.save()

        else:
            t_form = TaskForm()

    return HttpResponseRedirect(reverse("projects-detail", kwargs={"pk": pk}))