from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model extending Django's AbstractUser."""
    boss = models.ForeignKey(
        'self', on_delete=models.SET_DEFAULT, null=True, blank=True,
        related_name='subordinates', verbose_name='Boss',
        default=None)
    email = models.EmailField(unique=True, verbose_name='Email Address')
    first_name = models.CharField(max_length=50, default="test")
    last_name = models.CharField(max_length=50, default="test")
    full_name = models.CharField(max_length=50, null=True, blank=True,
                                 default=f"{first_name} {last_name}")

    def __str__(self):
        return self.username

    def get_direct_subordinates(self):
        """Return a queryset of direct subordinates."""
        return self.subordinates.all()

    def get_all_subordinates(self, collection=None):
        """Return a set of all subordinates, including indirect ones."""
        if collection is None:
            collection = set()

        direct_subordinates = self.get_direct_subordinates()

        for subordinate in direct_subordinates:
            if subordinate not in collection:
                collection.add(subordinate)
                subordinate.get_all_subordinates(collection)
        return collection
