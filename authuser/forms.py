from .models import User
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.forms.models import ModelForm


class Update_profile(ModelForm):
    """Form for updating user profile."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'boss']


class Update_password(SetPasswordForm):
    """Form for updating user password."""
    pass


class UserCreationForm(UserCreationForm):
    """Form for creating a new user."""
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'boss',
                  "password1", "password2"]
