from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from.models import Issue, Status 
from accounts.models import Role, Team, CustomUser
from .models import Issue, Status, Priority

from django.urls import reverse_lazy

from .models import Issue

class IssuePageView(ListView):
    model = Issue
    template_name = 'issues/issue.html'

    def populate_issue_list(self, name, staus, reporter, context):
        context[name] = Issue.objects.filter(
            status=status
        ).filter(
            reporter=reporter
        ).order_by(
            "created_on"
        ).reverse()


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
        to_do_status = Status.objects.get(name="To Do")
        in_progress_status = Status.objects.get(name="In Progress")
        done_status = Status.objects.get(name="Done")
        team = self.request.user.team
        role = Role.objects.get(name="Product Owner")
        product_owner = CustomUser.objects.filter(
            role=role).get(team=team)
            
        context["to_do"] = Issue.objects.filter(status=to_do_status)
        context["in_progress"] = Issue.objects.filter(status=in_progress_status)
        context["done"] = Issue.objects.filter(status=done_status)
        return context
