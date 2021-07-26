from django.shortcuts import render
from django.utils import timezone as tz
from datetime import date
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import Entry
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)

# Create your views here.

class EntryListView(ListView):
    model = Entry
    template_name = 'diary/home.html'
    context_object_name = 'entries'
    ordering = ['-date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        todays_entry = Entry.objects.get(date=date.today())
        context['todays_entry'] = todays_entry
        return context

class EntryCreateView(LoginRequiredMixin,CreateView):
    model = Entry
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(EntryCreateView, self).form_valid(form)


class EntryDetailView(LoginRequiredMixin, DetailView):
    model = Entry


class EntryUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Entry
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.author:
            return True
        return False

class EntryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Entry

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.author:
            return True
        return False

    def get_success_url(self):
        diary = self.object.diary_id
        return reverse_lazy('diary-home', args=(diary,))