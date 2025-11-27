from django.db import models
from apps.users.models import User

# Create your models here.
class Category(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories") 
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name