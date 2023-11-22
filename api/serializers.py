from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Task, Profile

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'task_content', 'state', 'worklist', 'date', 'worklist_date']
        extra_kwargs = {'title': {'required': False}, 'task_content':{'required':False}}

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'lastname']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', "profile"]