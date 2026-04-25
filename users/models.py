from django.db import models
from developer.models import *
# Create your models here.

class Wishlist(models.Model):
    user = models.ForeignKey(UserCreate, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'property']  # prevent duplicates

    def __str__(self):
        return f"{self.user} - {self.property}"



class Testimonial(models.Model):
    user = models.ForeignKey(UserCreate, on_delete=models.CASCADE)

    image = CloudinaryField(
        'image',
        folder="testimonials",
        null=True,
        blank=True
    )

    rating = models.DecimalField(max_digits=2, decimal_places=1)

    opinion = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    designation = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name

    # ✅ FIXED IMAGE LOGIC
    @property
    def display_image(self):

        # --------------------------------
        # 1. Testimonial uploaded image
        # --------------------------------
        if self.image:
            try:
                return self.image.url
            except Exception:
                pass


        # --------------------------------
        # 2. User profile uploaded image
        # --------------------------------
        try:
            if hasattr(self.user, "profile") and self.user.profile:

                profile = self.user.profile

                if profile.image:
                    img = str(profile.image)

                    # ignore old default vector
                    if (
                        img and
                        "Vector_te4oj7" not in img
                    ):
                        return profile.image.url

        except Exception:
            pass


        # --------------------------------
        # 3. Fallback initials avatar
        # same green theme as profile
        # --------------------------------
        name = (
            self.user.name
            or "User"
        ).strip()

        words = name.split()

        if len(words) >= 2:
            initials = (
                words[0][0] +
                words[1][0]
            ).upper()
        else:
            initials = name[:2].upper()


        return (
            "https://ui-avatars.com/api/"
            f"?name={initials}"
            "&background=8bc83f"
            "&color=ffffff"
            "&size=256"
            "&bold=true"
        )