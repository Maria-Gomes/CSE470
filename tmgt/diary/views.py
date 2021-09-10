from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponseRedirect
from django.utils import timezone as tz
from datetime import date
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import Entry
from .forms import EntryForm
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)

# Create your views here.

class EntryListView(ListView,LoginRequiredMixin,UserPassesTestMixin):
    model = Entry
    template_name = 'diary/home.html'
    context_object_name = 'entries'
    ordering = ['-date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entries'] = Entry.objects.filter(author=self.request.user)
        todays_entry = Entry.objects.filter(author=self.request.user,date__date=date.today()).order_by('-date__hour','-date__minute')
        context['todays_entry'] = todays_entry
        context['entry_form'] = EntryForm()
        return context

    def test_func(self):
        diary = self.get_object()
        if self.request.user == diary.author:
            return True
        return False

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
        entry = self.get_object()
        if self.request.user == entry.author:
            return True
        return False

class EntryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Entry

    def test_func(self):
        entry = self.get_object()
        if self.request.user == entry.author:
            return True
        return False

    def get_success_url(self):
        diary = self.request.user.pk
        return reverse_lazy('diary-home', args=(diary,))

def addEntry(request, pk):

    if request.method == 'POST':
        entry_form = EntryForm(request.POST)
        if entry_form.is_valid():
            entry = entry_form.save(commit=False)
            entry.author = request.user
            entry.date = date.today()
            entry.save()

        else:
            entry_form = EntryForm()

    return HttpResponseRedirect(reverse("diary-home", kwargs={"pk": pk}))