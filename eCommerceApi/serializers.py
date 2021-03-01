from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Product, Order, OrderDetail, ProductCategorie, ProductImage

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'password', 'groups']
        extra_kwargs = {
            'password':{
                'write_only':True,
                'required':True
            }
        }

    def create(self, validated_data):

        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ProductCategorieSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductCategorie
        fields = ['url', 'id', 'category']

class ProductImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['url', 'id', 'imageLink']

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['url', 'id', 'title', 'price', 'remainQuantity', 'description', 'hoverImage', 'productCategorie', 'productImage', 'user']

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ['url', 'id', 'firstName', 'lastName', 'companyName', 'countryName', 'shippingAddress', 'town', 'zipCode', 'phoneNo', 'orderComment', 'otherShippingAddress', 'paymentMethodType', 'subTotal', 'delivery', 'total', 'user', 'product']

class OrderDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ['url', 'order', 'product', 'orderedQuantity']