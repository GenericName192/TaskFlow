from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import ModelForm
from utility.utils import can_be_boss


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
                               """Can't do this it\
                                would cause circular hierarchy.""")
        self._validate_unique = True
        return self.cleaned_data


class UserCreationForm(UserCreationForm):
    """Form for creating a new user."""
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'boss',
                  "password1", "password2"]
