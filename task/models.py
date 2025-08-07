from django.db import models


# Create your models here.
class Task(models.Model):
    """Model representing a task."""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(
        'authuser.User', on_delete=models.CASCADE, null=False, blank=False,
        related_name='tasks', verbose_name='Assigned User')
    created_by = models.ForeignKey(
        'authuser.User', on_delete=models.CASCADE, null=False, blank=False,
        related_name='created_tasks', verbose_name='Created By')

    def __str__(self):
        return self.title
