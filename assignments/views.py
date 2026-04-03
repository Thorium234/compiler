from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Assignment

class LecturerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_lecturer

class AssignmentListView(LoginRequiredMixin, ListView):
    model = Assignment
    template_name = 'assignments/assignment_list.html'
    context_object_name = 'assignments'

    def get_queryset(self):
        return Assignment.objects.filter(created_by=self.request.user)

class AssignmentCreateView(LoginRequiredMixin, LecturerRequiredMixin, CreateView):
    model = Assignment
    template_name = 'assignments/assignment_form.html'
    fields = ['title', 'description', 'sample_input', 'expected_output']
    success_url = reverse_lazy('assignments:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
