from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import StaffSerializer, RegisterSerializer
from .models import Staff
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status


class StaffApi(APIView): 
    permission_classes = [IsAuthenticated]  # only authenticated users can access this view
    def get(self, request):
        queryset = Staff.objects.all()
        serializer = StaffSerializer(queryset,many=True)
        return Response({
            "status": True,
            "data": serializer.data
        })



class StaffAuthToken(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise AuthenticationFailed("Invalid credentials or inactive account")

        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.id, 'username': user.username, 'name': user.name})


class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully!",
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "username": user.username
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)