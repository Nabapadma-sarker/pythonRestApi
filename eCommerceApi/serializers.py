from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Product, Order, OrderDetail, ProductCategorie, ProductImage
from var_dump import var_dump
import json

class GroupSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Group
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):   
    groups = GroupSerializer(many=True)
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
        var_dump(groups_data)
        for group_data in groups_data:
            group = Group.objects.create(user=user, **group_data)
            user.groups.add(group)
        return user

    def update(self, instance,validated_data):
        groups_data = validated_data.pop('groups')
        password = validated_data.pop('password')
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.username)
        instance.set_password(password)
        instance.save()
        for group_data in groups_data:
            if 'id' in group_data.keys():
                if Group.objects.filter(id=group_data["id"]).exists():
                    group = Group.objects.get(id=group_data["id"])
                    var_dump(group)
                    group.name=group_data["name"]
                    group.save()
                    instance.groups.add(group)
                else:
                    continue
            else:
                group = Group.objects.create(user=instance, **group_data)
                user.groups.add(group)
        return instance
        

class RegisterSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'groups']
        extra_kwargs = {
            'password':{
                'write_only':True,
                'required':True
            },
            'email':{
                'required':True
            }
        }

    def create(self, validated_data):
        var_dump(validated_data)
        groups_data = validated_data.pop('groups')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        var_dump(groups_data)
        for group_data in groups_data:
            user.groups.add(group_data)
                
        return user

class ProductCategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategorie
        fields = ['url', 'id', 'category']

class ProductImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['url', 'id', 'imageLink', 'product']

class ProductSerializer(serializers.ModelSerializer):
    productImage = serializers.ListField(
                       child=serializers.FileField( max_length=100000,
                                         allow_empty_file=False,
                                         use_url=False ), write_only=True
                                )                 
                                
    productCategorie = serializers.CharField() 
    user = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    
    class Meta:
        model = Product
        productCategorie = ProductCategorie
        fields = ['url', 'id', 'title', 'price', 'remainQuantity', 'description', 'productCategorie', 'hoverImage', 'user', 'productImage']
    

    def create(self, validated_data):
        product_categories = json.loads(validated_data['productCategorie'])
        product_images = validated_data.pop('productImage')

        validated_data['user']=self.context['request'].user
        
        for product_categorie in product_categories:
            if 'id' in product_categorie.keys():
                if ProductCategorie.objects.filter(id=product_categorie["id"]).exists():
                    productCategorie = ProductCategorie.objects.get(id=product_categorie["id"])
                    var_dump(productCategorie)
                    validated_data['productCategorie']=productCategorie
                else:
                    continue
            else:
                productCategorie = ProductCategorie.objects.create(**product_categorie)
                validated_data['productCategorie']=productCategorie

        product = Product.objects.create(**validated_data)
        product.save()
        for product_image in product_images:
            productImage1 = ProductImage.objects.create(product=product, imageLink=product_image)
        return product

class ProductListSerializer(serializers.ModelSerializer):
    productImage = ProductImageSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Product
        fields = ['url', 'id', 'title', 'price', 'remainQuantity', 'description', 'productCategorie', 'hoverImage', 'user', 'productImage']
    
class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ['url', 'id', 'firstName', 'lastName', 'companyName', 'countryName', 'shippingAddress', 'town', 'zipCode', 'phoneNo', 'orderComment', 'otherShippingAddress', 'paymentMethodType', 'subTotal', 'delivery', 'total', 'user', 'product']

class OrderDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ['url', 'order', 'product', 'orderedQuantity']