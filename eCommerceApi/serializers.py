from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Product, Order, OrderDetail

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'price', 'remainQuantity', 'description', 'hoverImage', 'user']

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ['firstName', 'lastName', 'companyName', 'countryName', 'shippingAddress', 'town', 'zipCode', 'phoneNo', 'orderComment', 'otherShippingAddress', 'paymentMethodType', 'subTotal', 'delivery', 'total', 'user', 'product']

class OrderDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ['order', 'product']