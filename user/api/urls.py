from django.urls import path

from .views import SignupView, LoginView

app_name = 'user'
urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
]
