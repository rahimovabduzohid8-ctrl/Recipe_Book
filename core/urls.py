from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from core import views
from core.views import RecipeSearchView

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('recipe/list/', views.recipe_list, name='recipe_list'),
    path('recipe/detail/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/like/<int:pk>/', views.recipe_like, name='recipe_like'),
    path('recipe/wishlist/', views.wishlist_view, name='wishlist'),
    path('profile/', views.user_profile, name='my_profile'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('recipe/create/', views.recipe_create, name='recipe_create'),
    path('recipe/update/<int:pk>/', views.recipe_update, name='recipe_update'),
    path('recipe/delete/<int:pk>/', views.recipe_delete, name='recipe_delete'),
    path('search/', RecipeSearchView.as_view(), name='search'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)