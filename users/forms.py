from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class StudentRegistrationForm(UserCreationForm):
    assigned_lecturer = forms.ModelChoiceField(
        queryset=User.objects.filter(is_lecturer=True),
        required=False,
        label="Assign Lecturer",
        widget=forms.Select(attrs={'class': 'w-full p-2 mt-1 bg-slate-800 border border-slate-700 rounded-lg text-slate-200 outline-none focus:border-blue-500'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'assigned_lecturer')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        # assigned_lecturer is handled by the form field
        if commit:
            user.save()
        return user
