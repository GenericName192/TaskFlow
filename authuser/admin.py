from django.contrib import admin
from django.contrib.auth.models import Group
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken
from allauth.account.models import EmailAddress
from django.contrib.sites.models import Site
from .models import User


admin.site.register(User)


# unregister the unused models
admin.site.unregister(Group)
admin.site.unregister(SocialApp)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialToken)
admin.site.unregister(EmailAddress)
admin.site.unregister(Site)
