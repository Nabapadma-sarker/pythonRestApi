from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer, PostSerializer
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from mysite.models import Post, Comment


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

def register(request):
    form = UserCreationForm()
    context = {'form' : form}
    return render(request, 'register.html', context)

# def posts(request):
#     istekler = models.Post.objects.all()
#     return render(request, 'list.html', {'hh' : istekler})