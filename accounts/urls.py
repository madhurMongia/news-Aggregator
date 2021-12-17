from django.urls import path
from .views import RegistionView ,LoginView
app_name = 'accounts'
urlpatterns = [
    path('register/', RegistionView.as_view()),
    path('login/',LoginView.as_view())
]