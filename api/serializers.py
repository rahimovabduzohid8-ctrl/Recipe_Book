from rest_framework import serializers
from core.models import CustomUser, Recipe, Like, Comment


# Сериализатор пользователя (для отображения автора рецепта/комментария)
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'role']
        read_only_fields = ['role']


class RecipeSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'image', 'created_by',
            'created_at', 'updated_at', 'likes_count', 'comments_count',
            'is_liked_by_user'
        ]
        read_only_fields = ['created_at', 'updated_at', 'created_by']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_is_liked_by_user(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj.is_liked_by(request.user)


class LikeSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    recipe = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'recipe', 'created_at']
        read_only_fields = ['created_at']


class CommentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    recipe = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'recipe', 'user', 'text', 'created_at']
        read_only_fields = ['created_at', 'user']


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'image']