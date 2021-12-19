from django.db.models import query
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from .models import TechPost, EconomyPost, SportsPost, MarketPost
from next_prev import next_in_order, prev_in_order
from django.shortcuts import get_object_or_404
from .serializers import PostSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied, NotFound

def get_model(self):
        post_category = self.request.query_params.get('category', 'tech')
        get_category = {
            'tech': TechPost,
            'economy': EconomyPost,
            'stocks': MarketPost,
            'sports': SportsPost
        }
        if post_category not in get_category:
            raise NotFound(detail="Category not found")
        return get_category.get(post_category)
    
class CustomPageNumberPagination(PageNumberPagination):
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class customPermission(BasePermission):
    def has_permission(self, request, view):
        if int(request.query_params.get('page', 1)) >= 2 and not request.user.is_authenticated:
            return False
        return True


class PostList(GenericAPIView):

    serializer_class = PostSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [customPermission]

    def get_queryset(self):
        return get_model(self).objects.only(
            'headline', 'summary', 'slug', 'date_created').order_by("-date_created", 'pk')

    def get_page_size(self, request):
        if(request.user.is_authenticated):
            return 10
        return 5

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            self._paginator = self.pagination_class(
                page_size=self.get_page_size(self.request), page_query_param='page')
        return self._paginator

    def get(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(
            page, many=True, fields=('headline', 'summary', 'slug', 'date_created'),model = get_model(self))
        return self.get_paginated_response(serializer.data)


class PostDetails(GenericAPIView):
    serializer_class = PostSerializer
    def get_model(self,category):
        get_category = {
            'tech': TechPost,
            'economy': EconomyPost,
            'stocks': MarketPost,
            'sports': SportsPost
        }
        if category not in get_category:
            raise NotFound(detail="Category not found")
        return get_category.get(category)
        
    def get(self, request, slug,category):
        instance = get_object_or_404(self.get_model(category), slug=slug)
        queryset = self.get_model(category).objects.only(
            'slug', 'date_created').order_by("-date_created", 'pk')
        check = queryset[0:5]
        prev_post = prev_in_order(instance, qs=queryset)
        next_post = next_in_order(instance, qs=queryset)
        serializer = PostSerializer(instance ,model =self.get_model(category))
        if(not self.check_permission(request, check, slug)):
            raise PermissionDenied(detail="please login to view this post")
        return Response({'post': serializer.data,
                         'prev': prev_post.slug if prev_post else None,
                         'next': next_post.slug if next_post else None})

    def check_permission(self, request, qs, slug):
        if not request.user.is_authenticated:
            for object in qs:
                if(object.slug == slug):
                    return True
            return False
        return True
