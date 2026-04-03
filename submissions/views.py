from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from .services import run_python_code
from assignments.models import Assignment
from .models import Submission

@login_required
def editor_view(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    return render(request, 'submissions/editor.html', {'assignment': assignment})

@login_required
def practice_view(request):
    """Practice sandbox without specific assignment constraints."""
    return render(request, 'submissions/editor.html', {'is_practice': True})

@login_required
def execute_code_view(request):
    """Temporary test execution API."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            code = data.get('code', '')
            inputs = data.get('inputs', '')
            result = run_python_code(code, inputs)
            
            output = result.get('stdout', '')
            if result.get('stderr'):
                output += "\n--- Error Logs ---\n" + result['stderr']
                
            return JsonResponse({'output': output})
        except Exception as e:
            return JsonResponse({'output': f"API Error: {str(e)}"})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def flexible_compare(actual, expected):
    """Compare two strings ignoring trailing whitespace and final newlines."""
    def clean(s):
        if s is None: return ""
        # Split into lines, strip each line, join back, and strip overall
        lines = [line.rstrip() for line in s.splitlines()]
        return "\n".join(lines).strip()
    
    return clean(actual) == clean(expected)

@login_required
def submit_code_view(request, assignment_id):
    """Full submission and grading API."""
    if request.method == 'POST':
        assignment = get_object_or_404(Assignment, id=assignment_id)
        try:
            data = json.loads(request.body)
            code = data.get('code', '')
            
            # Execute with assignment's sample input
            sample_input = assignment.sample_input or ""
            result = run_python_code(code, sample_input)
            
            stdout = result.get('stdout', '')
            stderr = result.get('stderr', '')
            exit_code = result.get('exit_code', 0)
            
            # Compare with expected output
            passed = flexible_compare(stdout, assignment.expected_output)
            
            # Ensure no system errors count as a pass
            if exit_code != 0:
                passed = False

            # Save submission
            full_output = stdout
            if stderr:
                full_output += "\n--- Error Logs ---\n" + stderr
                
            Submission.objects.create(
                assignment=assignment,
                student=request.user,
                code=code,
                output=full_output,
                passed=passed
            )

            return JsonResponse({
                'output': full_output,
                'passed': passed
            })
        except Exception as e:
            return JsonResponse({'output': f"API Error: {str(e)}"}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def submission_list_scaffold(request):
    if request.user.is_lecturer or request.user.is_superuser:
        submissions = Submission.objects.all().order_by('-submitted_at')
        if not request.user.is_superuser:
             submissions = submissions.filter(assignment__created_by=request.user)
        return render(request, 'submissions/submission_list_scaffold.html', {'submissions': submissions})
    from django.http import HttpResponseForbidden
    return HttpResponseForbidden("Unauthorized")
