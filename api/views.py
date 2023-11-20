from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import Token, AccessToken, RefreshToken

from .serializers import TaskSerializer, UserSerializer, ProfileSerializer
from .models import Task, Profile

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name'] = user.profile.name
        token['lastname'] = user.profile.lastname

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class Login(APIView):
    def post(self, request, format=None):
        user = get_object_or_404(User, username=request.data["username"])
        if not user.check_password(request.data['password']):
            return Response({"detail":"Not found"}, status=status.HTTP_404_NOT_FOUND)

        tokens = RefreshToken().for_user(user)
        tokens_obj = {
            "refresh": str(tokens),
            "access": str(tokens.access_token),
        }

        return Response({"detail":"approved", "refresh":tokens_obj}, status=status.HTTP_201_CREATED)

class Signup(APIView):
    serializer_class = UserSerializer
    
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            user = User.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()

            profile = Profile.objects.create(user=user, name=request.data['name'], lastname=request.data['lastname'])

            refresh = RefreshToken.for_user(user)
            
            data = {
                "refresh":str(refresh),
                "access":str(refresh.access_token),
                "user": serializer.data,
            }
            return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    state = ['urgencia', 'pendente', 'concluido']

    def post(self, request, format=None):

        if request.data['state'].lower() not in self.state:
            return Response({"detail":"bad request"} ,status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"detail": "approved", "result": serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response({"detail": "not approved"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        task = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(task, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def put(self, request, pk, format=None):
        task = Task.objects.get(user=request.user, pk=pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        task = get_object_or_404(Task, user=request.user, pk=pk)
        task.delete()
        return Response(data={"detailt":"Item successfully deleted"}, status=status.HTTP_202_ACCEPTED)