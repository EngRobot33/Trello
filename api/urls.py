from django.urls import path, include

app_name = 'api'
urlpatterns = [
    path('trello/', include('trello.urls')),
    path('user/', include('user.urls')),
]
