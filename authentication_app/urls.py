from django.urls import path
from .views import CreateUserAPI, LoginAPIView, GoogleSocialAuthView,Hello,UserProfileView
from knox.views import LogoutView, LogoutAllView

urlpatterns = [
    path('create-user/', CreateUserAPI.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('logout-all/', LogoutAllView.as_view()),
    path('google/', GoogleSocialAuthView.as_view()),
    path('hello/',Hello.as_view()),
    path('profile/',UserProfileView.as_view({'post':'get_profile'})),
    path('changeName/',UserProfileView.as_view({'post':'change_name'}))
]
