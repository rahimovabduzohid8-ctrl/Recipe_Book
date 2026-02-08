from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecipeViewSet, CommentViewSet, LikeViewSet

router = DefaultRouter()

router.register(r'recipes', RecipeViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'likes', LikeViewSet, basename='likes')  # basename обязателен

urlpatterns = [
    path('', include(router.urls)),
]