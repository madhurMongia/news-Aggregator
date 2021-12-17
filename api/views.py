from rest_framework import pagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import  IsAuthenticated
from rest_framework.response import Response
from .models import TechPost
from rest_framework.pagination import PageNumberPagination
class PostList(ListAPIView):
    queryset = TechPost.objects.all()
    pagination_class = PageNumberPagination
    
class PostDetails(ListAPIView):
    permission_classes = [IsAuthenticated]
     
    def get(sef,request,slug):
        
        return Response()
