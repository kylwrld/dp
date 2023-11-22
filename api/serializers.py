from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Task, Profile
from django.utils import timezone

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'task_content', 'state', 'worklist', 'date', 'worklist_date']
        extra_kwargs = {'title': {'required': False}, 'task_content':{'required':False}} 

    def update(self, instance, validated_data):
        if "worklist" in validated_data and validated_data["worklist"] == True:
            instance.worklist_date = timezone.now()
        
        return super(TaskSerializer, self).update(instance, validated_data)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'lastname']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', "profile"]