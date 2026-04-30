from django.db import models
from developer.models import *
from developer.validators import *
import uuid
# Create your models here.

# class Wishlist(models.Model):
#     user = models.ForeignKey(UserCreate, on_delete=models.CASCADE)
#     property = models.ForeignKey(Property, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ['user', 'property']  # prevent duplicates

#     def __str__(self):
#         return f"{self.user} - {self.property}"


# class Wishlist(models.Model):

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

#     user = models.ForeignKey(
#         "developer.UserCreate",
#         on_delete=models.CASCADE,
#         related_name="wishlist"
#     )


#     property_uuid = models.UUIDField(null=True, blank=True)

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.email} - {self.property_uuid}"


# class Testimonial(models.Model):
#     user = models.ForeignKey(UserCreate, on_delete=models.CASCADE)

#     image = CloudinaryField(
#         'image',
#         folder="testimonials",
#         null=True,
#         blank=True
#     )

#     rating = models.DecimalField(max_digits=2, decimal_places=1)

#     opinion = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True)

#     designation = models.CharField(max_length=100, blank=True, null=True)

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.user.name

#     @property
#     def display_image(self):

#         if self.image:
#             try:
#                 return self.image.url
#             except Exception:
#                 pass

#         try:
#             if hasattr(self.user, "profile") and self.user.profile:

#                 profile = self.user.profile

#                 if profile.image:
#                     img = str(profile.image)

#                     if (
#                         img and
#                         "Vector_te4oj7" not in img
#                     ):
#                         return profile.image.url

#         except Exception:
#             pass


#         name = (
#             self.user.name
#             or "User"
#         ).strip()

#         words = name.split()

#         if len(words) >= 2:
#             initials = (
#                 words[0][0] +
#                 words[1][0]
#             ).upper()
#         else:
#             initials = name[:2].upper()


#         return (
#             "https://ui-avatars.com/api/"
#             f"?name={initials}"
#             "&background=8bc83f"
#             "&color=ffffff"
#             "&size=256"
#             "&bold=true"
#         )


class Wishlist(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        "developer.UserCreate",
        on_delete=models.CASCADE,
        related_name="wishlist"
    )

    property_uuid = models.UUIDField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.user:
            raise ValidationError("User is required.")

        if self.property_uuid and not isinstance(self.property_uuid, uuid.UUID):
            raise ValidationError("Invalid property UUID.")


    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} - {self.property_uuid}"



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


    def clean(self):

        if not self.user:
            raise ValidationError("User is required.")

        if self.rating is None:
            raise ValidationError("Rating is required.")

        if self.rating < 0 or self.rating > 5:
            raise ValidationError("Rating must be between 0 and 5.")

        validate_safe_text(self.opinion)

        if self.description:
            validate_safe_message(self.description)

        if self.designation:
            validate_safe_text(self.designation)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.name

    @property
    def display_image(self):

        if self.image:
            try:
                return self.image.url
            except Exception:
                pass

        try:
            if hasattr(self.user, "profile") and self.user.profile:

                profile = self.user.profile

                if profile.image:
                    img = str(profile.image)

                    if (
                        img and
                        "Vector_te4oj7" not in img
                    ):
                        return profile.image.url

        except Exception:
            pass

        name = (self.user.name or "User").strip()

        words = name.split()

        if len(words) >= 2:
            initials = (words[0][0] + words[1][0]).upper()
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