from django.forms.models import ModelForm
from .models import Task
from django import forms


class TaskForm(ModelForm):
    """Form for creating or updating a task."""
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={"cols": 30, "rows": 10})
        }
