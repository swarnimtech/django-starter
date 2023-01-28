from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, permissions, generics
from rest_framework import serializers


class HelloAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,format=None):
        return Response({
            "msg":"Good Morning"
        },status=status.HTTP_200_OK)
    
    def post(self,request,format=None):
        return Response({
            "username":request.user.username,
            "data":request.data
        }
        ,status=status.HTTP_200_OK)