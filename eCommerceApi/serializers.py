from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Product, Order, OrderDetail, ProductCategorie, ProductImage
from var_dump import var_dump

class GroupSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Group
        fields = ('url', 'name')

class UserSerializer(serializers.ModelSerializer):   
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'password', 'groups',)
        extra_kwargs = {
            'password':{
                'write_only':True,
                'required':True
            }
        }
    def create(self, validated_data):
        groups_data = validated_data.pop('groups')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        # user.groups.set(groups_data)
        for group_data in groups_data:
            var_dump(group_data.id)
            group = Group.objects.get(id=group_data.id)
            var_dump(group)
            # user.groups.add(group)
            group.user_set.add(user)
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