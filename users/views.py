from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import StudentRegistrationForm

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    
    def get_success_url(self):
        # Redirect based on role if needed, or default
        return '/users/dashboard/'

@login_required
def dashboard_view(request):
    user = request.user
    if user.is_lecturer:
        return render(request, 'users/lecturer_dashboard.html')
    elif user.is_student:
        from assignments.models import Assignment
        assignments = Assignment.objects.all()
        return render(request, 'users/student_dashboard.html', {'assignments': assignments})
    else:
        return render(request, 'users/dashboard.html') # default

def custom_logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('/users/login/')

@login_required
def lecturer_register_student_view(request):
    if not request.user.is_lecturer:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("Only lecturers can register students.")
        
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'users/register.html', {'form': form})
