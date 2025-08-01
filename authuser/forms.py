from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import ModelForm
from utility.utils import can_be_boss
from django import forms


class Update_profile(ModelForm):
    """Form for updating user profile."""
    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'boss']

    def clean(self):
        if self.cleaned_data.get('boss'):
            if not can_be_boss(self.user, self.cleaned_data.get('boss')):
                self.add_error("boss",
                               "Sorry, but this would cause a " +
                               "circular hierarchy. " +
                               "Please pick another user as your boss")
        self._validate_unique = True
        return self.cleaned_data


class AuthUserCreationForm(UserCreationForm):
    """Form for creating a new user."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add helpful help text
        self.fields['password1'].help_text = (
            "Choose a strong password with at least 8 characters. "
            "Mix letters, numbers, and symbols for better security."
        )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'boss',
                  "password1", "password2"]
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Choose a unique username'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter a unique email address'
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Your first name'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Your last name'
            }),
            'password1': forms.PasswordInput(attrs={
                'placeholder': 'At least 8 characters with letters and numbers'
            }),
            'password2': forms.PasswordInput(attrs={
                'placeholder': 'Confirm your password'
            }),
        }
        error_messages = {
            'email': {
                'unique': ("This email address is already registered. "
                           "Please use a different email or sign in instead.")
            },
            'password1': {
                'password_too_short': ("Please choose a longer password "
                                       "(at least 8 characters)."),
                'password_too_common': ("That password is too common. "
                                        "Try something more unique!"),
                'password_entirely_numeric': ("Passwords can't be only numbers"
                                              ". Please mix in letters too!"),
            }
        }

    # Custom error messages for form-level validation
    error_messages = {
        'password_mismatch': ("The passwords don't match. "
                              "Please try typing them again."),
    }
