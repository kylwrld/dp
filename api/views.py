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
import datetime


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name'] = user.profile.name
        token['lastname'] = user.profile.lastname
        token['username'] = user.username
        token['email'] = user.email

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class MyRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        token['name'] = user.profile.name
        token['lastname'] = user.profile.lastname
        token['username'] = user.username
        token['email'] = user.email

        return token

class Login(APIView):
    def post(self, request, format=None):
        if "username" in request.data:
            user = get_object_or_404(User, username=request.data["username"])
        elif "email" in request.data:
            user = get_object_or_404(User, email=request.data["email"])

        if not user.check_password(request.data['password']):
            return Response({"detail":"Not found"}, status=status.HTTP_404_NOT_FOUND)

        tokens = MyRefreshToken().for_user(user)
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

            Profile.objects.create(user=user, name=request.data['name'], lastname=request.data['lastname'])

            refresh = MyRefreshToken.for_user(user)
            
            data = {
                "refresh":str(refresh),
                "access":str(refresh.access_token),
                "user": serializer.data,
            }
            
            return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskView(APIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    state = ['urgencia', 'pendente', 'concluido']
    timedelta = datetime.timedelta(hours=-3)
    timezone = datetime.timezone(timedelta, "America/Sao_Paulo")

    def post(self, request, format=None):
        if request.data['worklist'] == True and len(Task.objects.filter(user=request.user, worklist=True)) == 3:
            self.worklist_swap(request)

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
        if "worklist" in request.data and request.data['worklist'] == True and len(Task.objects.filter(user=request.user, worklist=True)) == 3:
            self.worklist_swap(request)

        task = Task.objects.get(user=request.user, pk=pk)
        serializer = TaskSerializer(task, data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        task = get_object_or_404(Task, user=request.user, pk=pk)
        task.delete()
        return Response(data={"detailt":"Item successfully deleted"}, status=status.HTTP_202_ACCEPTED)
    
    def worklist_swap(self, request):
        worklist = Task.objects.filter(user=request.user, worklist=True)
        min = worklist[0].worklist_date
        j = 0
        for i in range(len(worklist)):
            if worklist[i].worklist_date < min:
                min = worklist[i].worklist_date
                j = i
        worklist[j].worklist = False
        worklist[j].save()