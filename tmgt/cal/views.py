from django.shortcuts import render, redirect
from django.db.models import Q
from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Event
from users.models import Notification
from projects.models import Tasks, Projects
from .forms import EventForm
from projects.forms import TaskForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    View
)

class EventListView(ListView):
    model = Event
    template_name = 'cal/home.html'
    context_object_name = 'events'
    ordering = ['-date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['e_form'] = EventForm()
        now = datetime.now()
        cal = HTMLCalendar().formatmonth(now.year, now.month)
        context['cal'] = cal
        tasks = Tasks.objects.filter(user=self.request.user, status="Incomplete", deadline__gte=now)
        context['tasks'] = tasks
        projects_id = []
        projects_title = []
        for task in tasks:
            projects_id.append(task.projects.pk)
            projects_title.append(task.projects.title)
        data = zip(tasks, projects_id, projects_title)
        context['data'] = data
        return context

class EventDetailView(DetailView):
    model = Event

class EventUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        event = self.get_object()
        if self.request.user == event.e_user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['e_form'] = EventForm(instance=self.get_object())
        return context


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    context_object_name = 'event'

    def test_func(self):
        event = self.get_object()
        if self.request.user == event.e_user:
            return True
        return False

    def get_success_url(self):
        user = self.request.user.id
        return reverse_lazy('calendar-home', args=(user,))

class EventNotifs(View):
    def get(self, request, notif_pk, event_pk, *args, **kwargs):
        notif = Notification.objects.get(pk=notif_pk)
        event = Event.objects.get(pk=event_pk)

        notif.notif_seen = True
        notif.save()

        return redirect('event-detail', event_pk)


@login_required(login_url='/')
def addEvent(request):

    if request.method == 'POST':
        e_form = EventForm(request.POST)
        if e_form.is_valid():
            event = e_form.save(commit=False)
            event.e_user = request.user
            event.save()
            pk = event.pk

        else:
            e_form = EventForm()
            events = Event.objects.filter(e_user= request.user)
            error = 'The form was not updated successfully. Please enter the fields correctly.'
            return render(request, 'cal/home.html', context={'e_form': e_form, 'events': events, 'error': error})

    return HttpResponseRedirect(reverse("calendar-home", kwargs={"pk": request.user.id}))
