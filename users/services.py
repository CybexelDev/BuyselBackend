from .models import UserCreate, UserProfile
from .utils import download_google_image


def handle_google_user(email, name, picture):
    # ✅ Create or get user
    user, created = UserCreate.objects.get_or_create(
        email=email,
        defaults={
            "name": name,
            "is_verified": True
        }
    )

    # ✅ If existing user → update name if empty
    if not created and not user.name:
        user.name = name
        user.save()

    # ✅ Profile
    profile, _ = UserProfile.objects.get_or_create(
        user=user,
        defaults={"auth_provider": "google"}
    )

    # ✅ Ensure provider
    if profile.auth_provider != "google":
        profile.auth_provider = "google"

    # ✅ Full name
    if not profile.full_name:
        profile.full_name = name

    # ✅ Save image only once
    if picture and not profile.image:
        image_file = download_google_image(picture, email)
        if image_file:
            profile.image.save(image_file.name, image_file, save=False)

    profile.save()

    return user, profile