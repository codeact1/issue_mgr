from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from.models import Issue, Status 

from django.urls import reverse_lazy

from .models import Issue

class IssuePageView(ListView):
    model = Issue
    template_name = 'issues/issue.html'

class IssueDetailView(DetailView):
    model = Issue
    template_name = 'issues/issue_detail.html' 

class IssueCreateView(LoginRequiredMixin, CreateView):
    model = Issue
    template_name = 'issues/new_issue.html'
    fields = ['title', 'description', 'priority', 'status', 'assigned_to']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class IssueUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Issue
    template_name = 'issues/edit_issue.html'
    fields = ['title', 'description', 'priority', 'status', 'assigned_to']

    def test_func(self):
        issue_obj = self.get_object()
        return self.request.user == issue_obj.created_by  

class IssueDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Issue
    template_name = 'issues/delete_issue.html'
    success_url = reverse_lazy('issue') 

class IssueListView(ListView):
    template_name = "issues/issue_list.html"
    model = Issue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = Status.objects.get(id=1)
        context["status"] = status
        return context
