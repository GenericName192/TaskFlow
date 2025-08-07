from django.forms.models import ModelForm
from .models import Task
from django import forms
from datetime import date


class TaskForm(ModelForm):
    """Form for creating or updating a task."""
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={"cols": 30, "rows": 10})
        }

    def clean(self):
        due_date = self.cleaned_data.get("due_date")
        if due_date:  # if a due_date has been set
            if due_date < date.today():
                self.add_error("due_date",
                               "You cannot set the due date "
                               + "to be in the past")
        return self.cleaned_data
