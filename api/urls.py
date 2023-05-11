from django.urls import path, include

app_name = 'api'
urlpatterns = [
    path('trello/', include('trello.api.urls')),
    path('user/', include('user.api.urls')),
]
