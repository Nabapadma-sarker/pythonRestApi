from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Products(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField(default=0, null=False)
    description = models.TextField(max_length=500)
    hoverImage = models.ImageField(upload_to='products')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Orders(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
