from django.shortcuts import render
from django.contrib.auth.models import User, Group
from .models import Product, Order, OrderDetail, ProductCategorie, ProductImage
from rest_framework import permissions, viewsets, serializers, generics
from .serializers import UserSerializer, GroupSerializer, ProductCategorieSerializer, ProductImageSerializer, ProductSerializer, OrderSerializer, OrderDetailSerializer, RegisterSerializer, ProductListSerializer
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.authtoken.views import obtain_auth_token,ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from var_dump import var_dump

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)


class UserIdWithAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class UserRegister(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny, )
    # parser_classes = [JSONParser]


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class ProductCategorieViewSet(viewsets.ModelViewSet):
    queryset = ProductCategorie.objects.all()
    serializer_class = ProductCategorieSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ProductListSerializer
            
        return ProductSerializer

class ProductUserwiseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def list(self, request):
        # var_dump(request.user)
        # queryset = Product.objects.filter(user=request)
        queryset = Product.objects.filter(user=request.user)
        serializer = ProductListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
        
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)
