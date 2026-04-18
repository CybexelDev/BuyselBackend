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

    image = models.ImageField(upload_to="testimonials/")
    rating = models.DecimalField(max_digits=2, decimal_places=1)

    opinion = models.CharField(max_length=255)   # one sentence
    description = models.TextField(blank=True, null=True)

    designation = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name