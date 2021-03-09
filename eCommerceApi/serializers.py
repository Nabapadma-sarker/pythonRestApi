from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Product, Order, OrderDetail, ProductCategorie, ProductImage
from var_dump import var_dump

class GroupSerializer(serializers.ModelSerializer):    
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Group
        fields = "__all__"

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
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class ProductCategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategorie
        fields = ['url', 'id', 'category']

class ProductImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['url', 'id', 'imageLink']

class ProductSerializer(serializers.ModelSerializer):
    productImage = serializers.ListField(
                       child=serializers.FileField( max_length=100000,
                                         allow_empty_file=False,
                                         use_url=False ), write_only=True
                                )                 
    # productImage = ProductImageSerializer(many=True)
    user = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    class Meta:
        model = Product
        fields = ['url', 'id', 'title', 'price', 'remainQuantity', 'description', 'productCategorie', 'hoverImage', 'user', 'productImage']
    

    def create(self, validated_data):
        # product_categories = validated_data.pop('productCategorie')
        product_images = validated_data.pop('productImage')
        var_dump(validated_data)
        var_dump(product_images)

        validated_data['user']=self.context['request'].user
        var_dump(self.context['request'].user.id)
        product = Product.objects.create(**validated_data)
        product.save()
        # var_dump(self.request.user)
        # for product_categorie in product_categories:
        #     if 'id' in product_categorie.keys():
        #         if ProductCategorie.objects.filter(id=product_categorie["id"]).exists():
        #             productCategorie = ProductCategorie.objects.get(id=group_data["id"])
        #             var_dump(productCategorie)
        #             productCategorie.category=product_categorie["category"]
        #             productCategorie.save()
        #             product.productCategorie.add(productCategorie)
        #         else:
        #             continue
        #     else:
        #         productCategorie = ProductCategorie.objects.create(user=product, **product_categorie)
        #         product.productCategorie.add(productCategorie)

        for product_image in product_images:
            var_dump(product_image)
            productImage = ProductImage.objects.create(imageLink=product_image)
            product.productImage.add(productImage)
        return product

class ProductListSerializer(serializers.ModelSerializer):
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