from django.contrib.auth.models import Group
from rest_framework import viewsets, response
from rest_framework import mixins, generics
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer
from users.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from . import serializers
from rest_framework.decorators import api_view
from .utils.square import Square


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]
    
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.MyTokenObtainPairSerializer
    
    
class CreateUserView(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = serializers.CreateUserSerializer
    
    def put(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@api_view(['GET'])
def list_catalog(request):
    location = request.user.location
    square = Square()
    items = square.list_all_items()
    items_to_display = []
    if location != None:
        for item in items:
            locations = item.get("locations")
            if location in locations:
                items_to_display.append(item)
    else:
        items_to_display = items

    return response.Response(items_to_display)