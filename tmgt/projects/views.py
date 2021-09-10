from datetime import datetime, date
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404, redirect
from django.template import RequestContext
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import Projects, Tasks, Comment
from users.models import Notification
from cal.models import Event
from .forms import TaskForm, CommentForm
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

class ProjectsListView(LoginRequiredMixin, ListView):
    model = Projects
    template_name = 'projects/home.html'
    context_object_name = 'projects'
    ordering = ['progress']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projects = Projects.objects.filter(author=self.request.user)
        context['projects'] = projects
        inc_tasks = []
        progress = []

        for project in projects:
            inc_tasks.append(Tasks.objects.filter(user=self.request.user, status='Incomplete', projects_id=project).count())
            progress.append(get_progress(project.pk))

        data = zip(inc_tasks, progress, projects)
        context['data'] = data

        now = datetime.now()
        tasks = Tasks.objects.filter(user=self.request.user, status='Incomplete', deadline=date.today())
        events = Event.objects.filter(e_user=self.request.user, date=date.today())
        comments = Comment.objects.filter(user_to=self.request.user)

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

        for comment in comments:
            existing_notif = Notification.objects.filter(notif_type=3, to_user=self.request.user,
                                                         from_user=comment.user_from, projects=comment.projects)
            if len(existing_notif) == 0:
                notif = Notification.objects.create(notif_type=3, to_user=self.request.user,
                                                    from_user=comment.user_from, projects=comment.projects)

        return context

class ProjectsDetailView(DetailView):
    model = Projects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Tasks.objects.filter(projects=self.object).order_by('-status')
        context['tasks'] = tasks
        context['t_form'] = TaskForm()
        context['comments'] = Comment.objects.filter(projects=self.object)
        context['c_form'] = CommentForm()
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
    fields = ['desc', 'deadline', 'submit_time']

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


class CommentNotifs(View):
    def get(self, request, notif_pk, project_pk, *args, **kwargs):
        notif = Notification.objects.get(pk=notif_pk)
        notif.projects = Projects.objects.get(pk=project_pk)

        notif.notif_seen = True
        notif.save()
        return redirect('projects-detail', notif.projects.pk)

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


@login_required(login_url='/')
def write_comment(request, pk):
    c_form = CommentForm(request.POST)
    if c_form.is_valid():
        comment = c_form.save(commit=False)
        comment.user_from = request.user
        projects = Projects.objects.get(pk=pk)
        comment.user_to = projects.author
        comment.projects = projects
        comment.save()

    else:
        c_form = CommentForm()

    return HttpResponseRedirect(reverse("projects-detail", kwargs = { "pk":pk }))

@login_required(login_url='/')
def completeTask(request, pk):
    task = Tasks.objects.get(pk=pk)

    if task.status == "Incomplete":
        task.status = "Complete"
    else:
        task.status = "Incomplete"

    task.save()

    return HttpResponseRedirect(reverse("projects-detail", kwargs= { "pk":task.projects.pk }))

def get_progress(project_pk):
    tasks = Tasks.objects.filter(projects=project_pk).count()
    if tasks == 0:
        return 0.0
    progress = (Tasks.objects.filter(projects=project_pk, status="Complete").count() / tasks) * 100
    project = Projects.objects.get(pk=project_pk)
    project.progress = progress
    project.save()

    return round(progress, 1)