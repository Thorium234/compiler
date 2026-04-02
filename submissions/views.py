from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def editor_view(request):
    return render(request, 'submissions/editor.html')

@login_required
def submission_list_scaffold(request):
    return render(request, 'submissions/submission_list_scaffold.html')
