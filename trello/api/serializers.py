from rest_framework import serializers

from user.models import User
from ..models import Project, Task


class TaskSerializer(serializers.ModelSerializer):
    assignees = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Task
        fields = ('title', 'description', 'project', 'assignees')


class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    managers = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    developers = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Project
        fields = ('title', 'tasks', 'description', 'managers', 'developers')
