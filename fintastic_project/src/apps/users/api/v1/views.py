from django.contrib.auth import get_user_model

from rest_framework import viewsets

from users.api.v1.serializers import UserSerializer

User = get_user_model()


class UserListViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    queryset = User.objects.all()
    serializer_class = UserSerializer
