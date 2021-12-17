from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from .models import TechPost
from next_prev import next_in_order, prev_in_order
from django.shortcuts import get_object_or_404
from .serializers import PostSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied

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
    queryset = TechPost.objects.only(
        'headline', 'summary', 'slug', 'date_created').order_by("-date_created", 'pk')
    pagination_class = CustomPageNumberPagination
    permission_classes = [customPermission]

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            self._paginator = self.pagination_class(
                page_size=10, page_query_param='page')
        return self._paginator

    def get(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(
            page, many=True, fields=('headline', 'summary', 'slug', 'date_created'))
        return self.get_paginated_response(serializer.data)


class PostDetails(GenericAPIView):
    serializer_class = PostSerializer

    def get(self, request, slug):
        instance = get_object_or_404(TechPost, slug=slug)
        queryset = TechPost.objects.only(
            'slug', 'date_created').order_by("-date_created", 'pk')
        check = queryset[0:10]
        prev_post = prev_in_order(instance, qs=queryset)
        next_post = next_in_order(instance, qs=queryset)
        serializer = PostSerializer(instance)
        if(not self.check_permission(request, check, slug)):
            raise PermissionDenied()
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
