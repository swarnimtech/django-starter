from django.urls import path

from .views import Hello

urlpatterns = [
    path('hello', Hello.as_view({'post': 'get_msg1'})),
    path('hello', Hello.as_view({'get': 'get_msg2'})),
]
