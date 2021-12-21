from django.urls import path
from .views import RegistionView, LoginView, VerificationView
app_name = 'accounts'
urlpatterns = [
    path('register/', RegistionView.as_view()),
    path('login/', LoginView.as_view()),
    path('verify/<str:token>', VerificationView.as_view())
]