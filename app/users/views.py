#views for user api

from rest_framework import generics

from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
#when users make http requests through URL, it will pass through createuserview class -> serailzer -> create object and return
