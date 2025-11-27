from django.db import models
from apps.users.models import User
import uuid

# Create your models here.
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories") 
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name