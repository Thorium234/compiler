from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import StudentRegistrationForm

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    
    def get_success_url(self):
        return '/users/dashboard/'

@login_required
def dashboard_view(request):
    user = request.user
    if user.is_lecturer or user.is_superuser:
        return render(request, 'users/lecturer_dashboard.html')
    elif user.is_student:
        from assignments.models import Assignment
        if user.assigned_lecturer:
            assignments = Assignment.objects.filter(created_by=user.assigned_lecturer)
        else:
            assignments = Assignment.objects.all()
        return render(request, 'users/student_dashboard.html', {'assignments': assignments})
    else:
        return render(request, 'users/dashboard.html')

def custom_logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('/users/login/')

@login_required
def lecturer_register_student_view(request):
    if not (request.user.is_lecturer or request.user.is_superuser):
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("Only lecturers or admins can register students.")
        
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            if request.user.is_lecturer:
                student.assigned_lecturer = request.user
            student.save()
            return redirect('users:dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def admin_register_lecturer_view(request):
    if not request.user.is_superuser:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("Only administrators can register lecturers.")
        
    from .forms import LecturerRegistrationForm
    if request.method == 'POST':
        form = LecturerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:dashboard')
    else:
        form = LecturerRegistrationForm()
    return render(request, 'users/register.html', {'form': form, 'title': 'Register Lecturer'})
