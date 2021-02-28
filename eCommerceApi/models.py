from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    remainQuantity = models.IntegerField(default=0, null=False)
    description = models.TextField(max_length=500)
    hoverImage = models.ImageField(upload_to='products')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    productCategorie = models.ForeignKey(ProductCategorie)
    productIamge = models.ManyToManyField(ProductIamge)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductCategorie(models.Model):
    category = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProductIamge(models.Model):
    imageLink = models.ImageField(upload_to='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    companyName = models.CharField(max_length=50)
    countryName = models.CharField(max_length=25)
    shippingAddress = models.CharField(max_length=255)
    town = models.CharField(max_length=50)
    zipCode = models.CharField(max_length=20)
    phoneNo = models.CharField(max_length=20)
    orderComment = models.CharField(max_length=255)
    otherShippingAddress = models.CharField(max_length=255, null=True)
    paymentMethodType = models.CharField(max_length=20)
    subTotal = models.IntegerField(default=0, null=False)
    delivery = models.IntegerField(default=0, null=False)
    total = models.IntegerField(default=0, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through='OrderDetail')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    orderedQuantity = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
