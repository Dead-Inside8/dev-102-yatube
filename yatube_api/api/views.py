from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action
from rest_framework.response import Response

from posts.models import Post, Comment, Follow, Group
from .serializers import PostSerializer, CommentSerializer, FollowSerializer, GroupSerializer
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с постами"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]  # <-- Измените на IsAuthorOrReadOnly
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с комментариями"""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]  # <-- Измените на IsAuthorOrReadOnly

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        serializer.save(author=self.request.user, post_id=post_id)


class FollowViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с подписками"""
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['following__username']

    # Разрешаем только list и create
    http_method_names = ['get', 'post', 'head', 'options']

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # Отключаем retrieve, update, partial_update, destroy
    def retrieve(self, request, *args, **kwargs):
        from rest_framework.response import Response
        return Response({'detail': 'Not found.'}, status=404)

    def update(self, request, *args, **kwargs):
        from rest_framework.response import Response
        return Response({'detail': 'Method not allowed.'}, status=405)

    def partial_update(self, request, *args, **kwargs):
        from rest_framework.response import Response
        return Response({'detail': 'Method not allowed.'}, status=405)

    def destroy(self, request, *args, **kwargs):
        from rest_framework.response import Response
        return Response({'detail': 'Method not allowed.'}, status=405)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для работы с группами (только чтение)"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.AllowAny]