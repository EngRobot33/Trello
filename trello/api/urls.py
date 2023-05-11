from django.urls import path

from .views import *

app_name = 'trello'
urlpatterns = [
    path('developer/tasks/', DeveloperTaskCreateAssignView.as_view(),
         name="create_assign_task"),
    path('developer/projects/<int:project_id>/tasks/', DeveloperTaskProjectRetrieveView.as_view(),
         name="retrieve_project_tasks"),
    path('manager/projects/', ProjectManagerCreateRetrieveProjectView.as_view(),
         name="add_retrieve_projects"),
    path('manager/projects/<int:project_id>/developer/<int:developer_id>/', ProjectManagerAssignProjectView.as_view(),
         name="assign_project"),
    path('manager/projects/<int:project_id>/', ProjectManagerCreateRetrieveTaskProjectView.as_view(),
         name="add_retrieve_tasks"),
    path('projects/<int:project_id>/tasks/', ProjectTasksListView.as_view(),
         name="project_tasks_list"),
    path('projects/<int:project_id>/developer/<int:developer_id>/tasks/', UsersTasksListView.as_view(),
         name="project_task_users_list"),
    path('manager/tasks/<int:task_id>/assign/developer/<int:developer_id>/', ProjectManagerAssignTaskView.as_view(),
         name="assign_task_developer"),
]
