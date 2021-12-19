from django.urls import path
from .views import PostDetails,PostList
app_name = 'api'

urlpatterns = [
    path('posts/', PostList.as_view(), name='posts'),
    path('post/<str:category>/<slug:slug>',
         PostDetails.as_view(), name='post-detail'),
]
