from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ProductCategorie(models.Model):
    category = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category

class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    remainQuantity = models.IntegerField(default=0, null=False)
    description = models.TextField(max_length=500)
    hoverImage = models.ImageField(upload_to='products')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    productCategorie = models.ForeignKey(ProductCategorie, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    imageLink = models.ImageField(upload_to='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productImage')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.imageLink)

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

    def __str__(self):
        return self.firstName + ' ' + self.lastName


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    orderedQuantity = models.IntegerField(default=0, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
