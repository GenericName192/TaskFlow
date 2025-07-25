from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import User


# Create your views here.
def index(request):
    """Render the index page."""
    return render(request, 'authuser/index.html')


@login_required
def profile(request, user_id):
    """Render the selected user profile page."""
    user = User.objects.get(id=user_id)
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
