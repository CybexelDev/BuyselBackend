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


