

from django.urls import path, include
from rest_framework import routers
from eCommerceApi import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('groups', views.GroupViewSet)
router.register('product-categorie', views.ProductCategorieViewSet)
router.register('Product-image', views.ProductImageViewSet)
router.register('products', views.ProductViewSet)
router.register('products-user', views.ProductUserwiseViewSet)
router.register('orders', views.OrderViewSet)
router.register('ordergroups', views.OrderDetailViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('register/', views.UserRegister.as_view())
]