from datetime import datetime, date

from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404, redirect
from django.template import RequestContext
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import Projects, Tasks
from users.models import Notification
from cal.models import Event
from .forms import TaskForm
from django.db.models import F
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    View
)


# Create your views here.

class ProjectsListView(ListView):
    model = Projects
    template_name = 'projects/home.html'
    context_object_name = 'projects'
    ordering = ['progress']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = datetime.now()
        tasks = Tasks.objects.filter(user=self.request.user, status='Incomplete', deadline=date.today())
        events = Event.objects.filter(e_user=self.request.user, date=date.today())

        for task in tasks:
            time = task.submit_time.hour-2
            existing_notif = Notification.objects.filter(notif_type=1,to_user=self.request.user,
                                                         task=task, date__hour__lt=time)
            if task.submit_time >= now.time() and len(existing_notif) == 0:
                existing_notif = Notification.objects.filter(notif_type=1, to_user=self.request.user,
                                                             task=task, date__hour__gte=time)
                if len(existing_notif) == 0:
                    notif = Notification.objects.create(notif_type=1, to_user=self.request.user, task=task)

        for event in events:
            time = event.start_t.hour - 1
            existing_notif = Notification.objects.filter(notif_type=2,to_user=self.request.user,
                                                         event=event, date__hour__lt=time)
            if event.start_t.hour >= now.hour and len(existing_notif) == 0:
                existing_notif = Notification.objects.filter(notif_type=2, to_user=self.request.user,
                                                             event=event, date__hour__gte=time)
                if len(existing_notif) == 0:
                    notif = Notification.objects.create(notif_type=2, to_user=self.request.user, event=event)

        return context

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
    fields = ['desc', 'deadline', 'status', 'submit_time']

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

class TaskNotifs(View):
    def get(self, request, notif_pk, task_pk, *args, **kwargs):
        notif = Notification.objects.get(pk=notif_pk)
        task = Tasks.objects.get(pk=task_pk)

        notif.notif_seen = True
        notif.save()
        return redirect('projects-detail', task.projects.pk)


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


# @login_required(login_url='/')
# def write_comment(request, pk):
#     c_form = CommentForm(request.POST)
#     if c_form.is_valid():
#         comment = c_form.save(commit=False)
#         comment.user = request.user
#         comment.project = Projects.objects.get(pk=pk)
#         comment.save()
#
#     else:
#         c_form = CommentForm()
#
#     return HttpResponseRedirect(reverse("project-detail", kwargs = { "pk":pk }))