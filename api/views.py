from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from core.models import Recipe, Like, Comment
from .serializers import RecipeSerializer, LikeSerializer, CommentSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Рецепты (список, детали, создание, лайк)"""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)  # для загрузки фото

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.query_params.get('q')  # поиск по названию/описанию
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q)
            )
        return qs

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        """Поставить/убрать лайк"""
        recipe = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, recipe=recipe)
        if not created:
            like.delete()
            return Response({
                'liked': False,
                'likes_count': recipe.likes.count()
            })
        return Response({
            'liked': True,
            'likes_count': recipe.likes.count()
        })


class CommentViewSet(viewsets.ModelViewSet):
    """Комментарии к рецептам"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeViewSet(viewsets.ReadOnlyModelViewSet):
    """Лайки текущего пользователя"""
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user)