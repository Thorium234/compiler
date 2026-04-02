from django.contrib import admin
from .models import Submission

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'passed', 'submitted_at')
    list_filter = ('passed', 'assignment')
