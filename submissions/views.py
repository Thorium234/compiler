from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from .services import run_python_code

@login_required
def editor_view(request):
    return render(request, 'submissions/editor.html')

@login_required
def submission_list_scaffold(request):
    return render(request, 'submissions/submission_list_scaffold.html')

@login_required
def execute_code_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            code = data.get('code', '')
            inputs = data.get('inputs', '')
            output = run_python_code(code, inputs)
            return JsonResponse({'output': output})
        except Exception as e:
            return JsonResponse({'output': f"API Error: {str(e)}"})
    return JsonResponse({'error': 'Invalid request'}, status=400)
