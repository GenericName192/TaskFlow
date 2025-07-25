from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from .forms import Update_profile, Update_password, UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.
def index(request):
    """Render the index page."""
    return render(request, 'authuser/index.html')


@login_required
def profile(request, user_id):
    """Render the selected user profile page."""
    user = get_object_or_404(User, id=user_id)
    subordinates = (
        user
        .get_direct_subordinates()
        .prefetch_related('subordinates')
    )

    subordinates_dict = {}
    for subordinate in subordinates:
        subordinates_dict[
            subordinate] = list(
            subordinate.get_direct_subordinates()
        )

    return render(request, 'authuser/profile.html',
                  {
                      'user_profile': user,
                      'subordinates_dict': subordinates_dict
                  })


@login_required
def edit_profile(request, user_id):
    if request.user.id != user_id:
        return render(request, 'authuser/unauthorized.html')

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


@login_required
def change_password(request, user_id):
    if request.user.id != user_id:
        return render(request, 'authuser/unauthorized.html')

    user = get_object_or_404(User, id=user_id)
    form = Update_password(user=user)
    if request.method == 'POST':
        form = Update_password(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password changed successfully!')
            return redirect('profile', user_id=user.id)
    return render(request, 'authuser/update_password.html',
                  {'user': user, 'form': form})


def register(request):
    """Render the registration page."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
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


@login_required
def logout_view(request):
    """Handle user logout."""
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('index')


def login_view(request):
    """Render the login page."""
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
