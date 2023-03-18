from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from authentication_app import google
from authentication_app.register import register_social_user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
        extra_kwargs = {"password": {"required": True}}

    def validate(self, data):
        email = data.get("email", "").strip().lower()
        name = data.get("first_name")
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with email already exists')
        if not name:
            raise serializers.ValidationError("Please Provide a User name")
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email').lower()
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError("Please give both email and password.")

        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email does not exist.')

        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if not user:
            raise serializers.ValidationError("Wrong Credentials.")

        attrs['user'] = user
        return attrs


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        # Check if the user has sent the auth token from our website
        # if user_data['aud'] != config('GOOGLE_CLIENT_ID'):
        #     raise AuthenticationFailed('oops, who are you?')

        first_name = user_data['given_name']
        last_name = user_data['family_name']
        email = user_data.get('email', 'dummy@gmail.com')
        provider = 'google'

        user = register_social_user(
            provider=provider, email=email, first_name=first_name, last_name=last_name)

        return user
