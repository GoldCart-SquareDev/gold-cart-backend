from django.contrib.auth.models import Group
from rest_framework import viewsets, response, views
from rest_framework import mixins, generics, permissions, status
from .serializers import UserSerializer, GroupSerializer
from users.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from . import serializers
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .utils.square import Square

square = Square()

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]


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


@api_view(["GET"])
def list_catalog(request):
    items = square.list_all_items()
    items_to_display = []
    if request.user.is_authenticated: 
        location = request.user.location
        if location:
            for item in items:
                locations = item.get("locations")
                if locations and location in locations:
                    items_to_display.append(item)
        else:
            items_to_display = items
        return response.Response(items_to_display, status=status.HTTP_200_OK)
    return response.Response(items, status=status.HTTP_200_OK)


@api_view(["POST"])
def checkout(request):
    if request.user.is_authenticated:
        print(dict(request.POST)["item_id"])
        #serializer = serializers.LineItemDictionarySerializer(request.POST, many=True)
        #print(serializer.data)
        basket = dict(request.POST)
        location_id = basket["location_id"][0]
        line_items = []
        for quantity, item_id  in zip(basket["quantity"], basket["item_id"]):
            line_items.append({'quantity': quantity, "catalog_object_id": item_id})
        url = square.checkout(line_items=line_items, location_id=location_id)
        if url:
            return response.Response({"url": url}, status=status.HTTP_200_OK)
        return response.Response("error", status=status.HTTP_400_BAD_REQUEST)
    return response.Response("error", status=status.HTTP_403_FORBIDDEN)