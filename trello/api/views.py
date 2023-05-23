from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Project, Task
from .serializers import TaskSerializer, ProjectSerializer

from user.models import User
from user.permissions import IsProjectManager, IsDeveloper


class DeveloperTaskCreateAssignView(APIView):
    permission_classes = [IsDeveloper]

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            task = serializer.save()
            task.assignees.add(user)
            task.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeveloperTaskProjectRetrieveView(APIView):
    permission_classes = [IsDeveloper]

    def get(self, request, project_id):
        tasks = Task.objects.filter(project=project_id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(data=serializer.data)


class ProjectManagerCreateRetrieveProjectView(APIView):
    permission_classes = [IsProjectManager]

    def get(self, request):
        projects = Project.objects.filter(managers=request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(data=serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(id=request.user.id)
            project = serializer.save()
            project.managers.add(user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectManagerAssignProjectView(APIView):
    permission_classes = [IsProjectManager]

    def post(self, request, project_id, developer_id):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response(data={'Database Error': ['Project not found!']}, status=status.HTTP_404_NOT_FOUND)

        try:
            developer = User.objects.get(id=developer_id)
        except User.DoesNotExist:
            return Response(data={'Database Error': ['Developer not found!']}, status=status.HTTP_404_NOT_FOUND)

        project.developers.add(developer)
        project.save()
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectManagerCreateRetrieveTaskProjectView(APIView):
    permission_classes = [IsProjectManager]

    def get_project(self, project_id):
        try:
            return Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return None

    def get_tasks(self, project, user):
        if user.role == User.PROJECT_MANAGER:
            return project.tasks.all()
        else:
            return project.tasks.filter(assignees=user)

    def get(self, request, project_id):
        project = self.get_project(project_id)
        if project is None:
            return Response(data={"Database Error": "Project not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        tasks = self.get_tasks(project, user)

        data = {"project": project.title, "tasks": []}
        for task in tasks:
            task_data = {"title": task.title, "description": task.description}
            data["tasks"].append(task_data)

        return Response(data=data)

    def post(self, request, project_id):
        project = self.get_project(project_id)
        if project is None:
            return Response(data={"Database Error": "Project not found."}, status=status.HTTP_404_NOT_FOUND)

        title = request.data.get("title")
        description = request.data.get("description")

        if not title:
            return Response(data={"Database Error": "Title is required."}, status=status.HTTP_400_BAD_REQUEST)

        task = Task.objects.create(title=title, description=description, project=project)
        data = {"title": task.title, "description": task.description}
        return Response(data=data, status=status.HTTP_201_CREATED)


class ProjectTasksListView(APIView):
    permission_classes = [IsProjectManager, IsDeveloper]

    def get(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        tasks = Task.objects.filter(project=project)
        serializer = TaskSerializer(tasks, many=True)
        return Response(data=serializer.data)


class UsersTasksListView(APIView):
    permission_classes = [IsProjectManager]

    def get(self, request, developer_id, project_id):
        user = get_object_or_404(User, id=developer_id)
        project = get_object_or_404(Project, id=project_id)
        tasks = Task.objects.filter(project=project, assignees=user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(data=serializer.data)


class ProjectManagerAssignTaskView(APIView):
    permission_classes = [IsProjectManager]

    def post(self, request, task_id, developer_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            assignee = User.objects.get(id=developer_id)
        except User.DoesNotExist:
            return Response(data={"Database Error": ["Invalid user ID."]}, status=status.HTTP_404_NOT_FOUND)

        task.assignees.add(assignee)
        task.save()
        serializer = TaskSerializer(task)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
