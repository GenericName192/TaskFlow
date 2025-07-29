from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from .forms import Update_profile, UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm


# Create your views here.
def index(request):
    """Render the index page."""
    total_tasks_count = request.user.tasks.count()
    total_completed_tasks = request.user.tasks.filter(completed=True).count()
    total_ongoing_tasks = total_tasks_count - total_completed_tasks
    up_coming_tasks = request.user.tasks.all().order_by("due_date")
    return render(request, 'authuser/index.html',
                  {
                      "total_tasks_count": total_tasks_count,
                      "total_completed_tasks": total_completed_tasks,
                      "total_ongoing_tasks": total_ongoing_tasks,
                      "up_coming_tasks": up_coming_tasks
                  })


@login_required(login_url='login_view')
def profile(request, user_id):
    """Render the selected user profile page."""
    user = get_object_or_404(User, id=user_id)
    direct_subordinates = user.get_direct_subordinates()
    all_subordinates = user.get_all_subordinates()

    return render(request, 'authuser/profile.html',
                  {
                      'user_profile': user,
                      'direct_subordinates': direct_subordinates,
                      'all_subordinates': all_subordinates
                  })


@login_required(login_url='login_view')
def edit_profile(request, user_id):
    if request.user.id != user_id:
        messages.error(request, 'You are not authorized to edit this profile.')
        return redirect('index')

    user = get_object_or_404(User, id=user_id)
    form = Update_profile(instance=user)
    if request.method == 'POST':
        form = Update_profile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile', user_id=user.id)

    return render(request, 'authuser/edit_profile.html',
                  {'user': user, 'form': form})


@login_required(login_url='login_view')
def change_password(request, user_id):
    if request.user.id != user_id:
        messages.error(request, 'You cannot change someone else\'s password.')
        return redirect('index')

    user = get_object_or_404(User, id=user_id)
    form = PasswordChangeForm(user=user)
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=user.username,
                password=form.cleaned_data['new_password1']
            )
            login(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('profile', user_id=user.id)

    return render(request, 'authuser/update_password.html',
                  {'user': user, 'form': form})


def register(request):
    """Render the registration page."""
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('index')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save
            form.save()
            messages.success(
                request, 'Account created successfully! Welcome to TaskFlow!'
            )
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'authuser/register.html', {'form': form})


@login_required(login_url='login_view')
def logout_view(request):
    """Handle user logout."""
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('index')


def login_view(request):
    """Render the login page."""
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('index')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                messages.success(request, 'Welcome back!')
                return redirect('index')
    else:
        form = AuthenticationForm()

    return render(request, 'authuser/login.html', {'form': form})
