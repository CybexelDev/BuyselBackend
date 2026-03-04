# yourapp/signals.py

from allauth.socialaccount.signals import social_account_added
from django.dispatch import receiver
from .models import UserProfile


@receiver(social_account_added)
def update_provider(request, sociallogin, **kwargs):

    email = sociallogin.user.email
    provider = sociallogin.account.provider  # google / facebook

    try:
        profile = UserProfile.objects.get(user__email=email)
        profile.auth_provider = provider
        profile.save()
    except UserProfile.DoesNotExist:
        pass