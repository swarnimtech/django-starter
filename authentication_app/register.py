from django.contrib.auth import authenticate
from authentication_app.models import CustomUser
from rest_framework.exceptions import AuthenticationFailed
from decouple import config


def register_social_user(provider, email, first_name, last_name):
    filtered_user_by_email = CustomUser.objects.filter(email=email)

    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:

            registered_user = authenticate(
                email=email, password=config('SOCIAL_SECRET'))

            return registered_user

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
        user = {
            'email': email,
            'password': config('SOCIAL_SECRET'),
            'first_name': first_name,
            'last_name': last_name
        }
        user = CustomUser.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()

        new_user = authenticate(email=email, password=config('SOCIAL_SECRET'))
        return new_user
