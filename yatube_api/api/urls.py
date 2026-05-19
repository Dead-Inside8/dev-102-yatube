from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CommentViewSet, FollowViewSet, GroupViewSet

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('follow', FollowViewSet, basename='follow')
router.register('groups', GroupViewSet, basename='groups')  # <-- Добавляем группы

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_id>/comments/', CommentViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='comments'),
    path('posts/<int:post_id>/comments/<int:pk>/', CommentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='comment-detail'),
]