from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from .models import User


admin.site.register(User)


# unregister the unused models
admin.site.unregister(Group)
admin.site.unregister(Site)
