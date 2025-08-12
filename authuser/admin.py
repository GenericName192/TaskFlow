from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from .models import User
from django.contrib.auth.admin import UserAdmin


class authUser(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'boss')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
        ('Important dates', {'fields': ('date_joined',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name',
                       'boss', 'password1', 'password2'),
        }),
    )

    readonly_fields = ('date_joined',)


admin.site.register(User, authUser)


# unregister the unused models
admin.site.unregister(Group)
admin.site.unregister(Site)
