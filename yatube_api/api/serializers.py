from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Post, Follow, Group
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)  # <-- Добавьте эту строку

    class Meta:
        fields = '__all__'
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок"""
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ['user', 'following']

    def validate_following(self, value):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and value == request.user:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        return value

    def validate(self, data):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            if Follow.objects.filter(
                    user=request.user,
                    following=data['following']
            ).exists():
                raise serializers.ValidationError(
                    {'following': 'Вы уже подписаны на этого пользователя'}
                )
        return data


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'title', 'slug', 'description']  # Явно укажите поля