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

        # ✅ 1. If testimonial image exists → use it
        if self.image:
            return self.image.url

        # ✅ 2. If user profile has REAL image (not default)
        if hasattr(self.user, "profile") and self.user.profile.image:
            profile_img = str(self.user.profile.image)

            # ❗ Skip default image
            if "Vector_te4oj7" not in profile_img:
                return self.user.profile.image.url

        # ✅ 3. Final fallback
        return "https://res.cloudinary.com/dobvmpgiw/image/upload/Vector_te4oj7"