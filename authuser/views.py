from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import User
from .forms import Update_profile, AuthUserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .tips import get_tip
from utility.constants import (
    LOGIN_URL_NAME, INDEX_URL_NAME, PROFILE_URL_NAME,
    INDEX_TEMPLATE, PROFILE_TEMPLATE, EDIT_PROFILE_TEMPLATE,
    LOGIN_TEMPLATE, REGISTER_TEMPLATE, UPDATE_PASSWORD_TEMPLATE
)
from utility.utils import calculate_user_task_statistics
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    """Render the index page."""
    if request.user.is_authenticated:
        content = calculate_user_task_statistics(request.user)
        tip = get_tip()
        content["tip"] = tip
    else:
        content = {}
    return render(request, INDEX_TEMPLATE, content)


@login_required(login_url=LOGIN_URL_NAME)
def profile(request, user_id: int):
    """Render the selected user profile page."""
    user = get_object_or_404(User.objects.prefetch_related("subordinates"),
                             id=user_id)
    dirct_sub = Paginator(user.subordinates.all(), 5)
    direct_sub_page = request.GET.get("direct_sub_page")
    direct_subordinates = dirct_sub.get_page(direct_sub_page)

    # Convert set to list for pagination
    all_subordinates_set = user.get_all_subordinates()
    all_sub_count = len(all_subordinates_set)
    all_sub = Paginator(list(all_subordinates_set), 6)
    all_sub_page = request.GET.get("all_sub_page")
    all_subordinates = all_sub.get_page(all_sub_page)

    return render(request, PROFILE_TEMPLATE,
                  {
                      'user_profile': user,
                      'direct_subordinates': direct_subordinates,
                      'all_subordinates': all_subordinates,
                      "all_sub_count": all_sub_count
                  })


@login_required(login_url=LOGIN_URL_NAME)
def edit_profile(request, user_id: int):
    """ Renders a form that allows the user to update all user infomation
    exepct for password.
    """
    if request.user.id != user_id:
        raise PermissionDenied("""You do not have permission\
                               to edit this profile""")

    user = get_object_or_404(User, id=user_id)
    form = Update_profile(instance=user, user=request.user)
    if request.method == 'POST':
        form = Update_profile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect(PROFILE_URL_NAME, user_id=user.id)

    return render(request, EDIT_PROFILE_TEMPLATE,
                  {'user': user, 'form': form})


@login_required(login_url=LOGIN_URL_NAME)
def change_password(request, user_id: int):
    """Renders a form to allow the user to change their password."""
    if request.user.id != user_id:
        raise PermissionDenied("""You do not have permission\
        to change this password""")

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
            return redirect(PROFILE_URL_NAME, user_id=user.id)

    return render(request, UPDATE_PASSWORD_TEMPLATE,
                  {'user': user, 'form': form})


def register(request):
    """Render the registration page."""
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect(INDEX_URL_NAME)

    if request.method == 'POST':
        form = AuthUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, 'Account created successfully! Welcome to TaskFlow!'
            )
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            if user is not None:
                login(request, user)
                return redirect(INDEX_URL_NAME)
    else:
        form = AuthUserCreationForm()
    return render(request, REGISTER_TEMPLATE, {'form': form})


@login_required(login_url=LOGIN_URL_NAME)
def logout_view(request):
    """Handle user logout."""
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect(INDEX_URL_NAME)


def login_view(request):
    """Render the login page."""
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect(INDEX_URL_NAME)

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # If form is valid, the user exists and password is correct
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Welcome back!')
            return redirect(INDEX_URL_NAME)
        # If form is not valid, it will contain the authentication errors
    else:
        form = AuthenticationForm()

    return render(request, LOGIN_TEMPLATE, {'form': form})
