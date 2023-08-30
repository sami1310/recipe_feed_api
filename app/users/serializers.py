from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name'] #fields that users are allowed to change
        extra_kwargs = {'password':{'write_only': True,'min_length': 5}} #extra fields with read/write only permissions,validation error that users are allowed to cvhange

     #overidding the create_user method from UserManager for saving encrypted password in the database after user creates profile
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

