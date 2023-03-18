from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets

# Create your views here.
class Hello(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_msg1(self, request, format=None):
        return Response("Hello World 1")
    
    def get_msg2(self, request, format=None):
        return Response("Hello World 2")