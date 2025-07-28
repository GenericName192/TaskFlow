from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from django.contrib import messages
from authuser.models import User


@login_required(login_url='login_view')
def task_list(request, user_id):
    """Render the task list page."""
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.assigned_to = user
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('task_list', user_id=user.id)
    else:
        form = TaskForm()
        ongoing_tasks = user.tasks.filter(completed=False)
        completed_tasks = user.tasks.filter(completed=True)
        return render(request, 'task/task_list.html',
                      {'user': user,
                       'ongoing_tasks': ongoing_tasks,
                       'completed_tasks': completed_tasks,
                       'form': form})
