from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from .serializers import CreateUserSerializer, LoginSerializer, GoogleSocialAuthSerializer
from .models import CustomUser
from knox import views as knox_views
from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets


class Hello(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response("Hello World")

# Create your views here.
class CreateUserAPI(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)


class UserProfileView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_profile(self,request):
        return Response({
            "email":request.user.email,
            "firstName":request.user.first_name,
            "lastName":request.user.last_name,
        })
    
    def change_name(self, request):
        data = request.data
        myuser=CustomUser.objects.get(id=request.user.id)
        firstName = data["firstName"]
        lastName = data["lastName"]
        
        if(firstName and lastName):
            myuser.first_name = firstName
            myuser.last_name = lastName
            myuser.save()
            return Response("Saved SuccessFully")

        return Response("Failed to Save",status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(knox_views.LoginView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)
            response = super().post(request, format=None)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response(response.data, status=status.HTTP_200_OK)


class GoogleSocialAuthView(knox_views.LoginView):
    permission_classes = (AllowAny,)
    serializer_class = GoogleSocialAuthSerializer

    def post(self, request, format=None):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['auth_token']
            login(request, user)
            response = super().post(request, format=None)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response(response.data, status=status.HTTP_200_OK)
