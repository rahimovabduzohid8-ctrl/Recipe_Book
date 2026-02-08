from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.views.generic import ListView
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST

from core.models import Recipe, Like, Comment
from core.form import RecipeForm, CommentForm


def home(request):
    recipe_count = Recipe.objects.count()
    return render(request, "base.html", {"recipe_count": recipe_count})

User = get_user_model()

@login_required
def user_profile(request, username=None):
    if username is None:
        user = request.user
    else:
        user = get_object_or_404(User, username=username)
    recipes = Recipe.objects.filter(created_by=user).order_by('-created_at')

    context = {
        'profile_user': user,
        'recipes': recipes,
        'recipe_count': recipes.count(),
        'is_own_profile': user == request.user,
    }

    return render(request, 'profile.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, "Неверный логин или пароль.")

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'list.html', {'recipes': recipes})


class RecipeSearchView(ListView):
    model = Recipe
    template_name = 'search.html'
    context_object_name = 'recipes'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '').strip()

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
        else:
            queryset = queryset.none()  # если нет запроса — пусто

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


@login_required(login_url='/login/')
@require_POST
def recipe_like(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    # Проверяем, есть ли уже лайк
    existing_like = Like.objects.filter(recipe=recipe, user=request.user).first()

    if existing_like:
        existing_like.delete()
        messages.success(request, "Лайк убран.")
    else:
        Like.objects.create(recipe=recipe, user=request.user)
        messages.success(request, "Лайк поставлен! ❤️")

    # Возвращаем на предыдущую страницу
    return redirect(request.META.get('HTTP_REFERER', 'recipe_list'))


@login_required(login_url='/login/')
def wishlist_view(request):
    wishlist_recipes = Recipe.objects.filter(likes__user=request.user).distinct()
    wishlist_recipes = wishlist_recipes.order_by('-likes__created_at')

    context = {
        'wishlist_recipes': wishlist_recipes,
    }
    return render(request, 'wishlist.html', context)


@login_required(login_url='/login/')
def recipe_create(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.created_by = request.user
            recipe.save()
            messages.success(request, "Рецепт успешно добавлен!")
            return redirect('recipe_list')
        else:
            messages.error(request, "Проверьте поля формы.")
    else:
        form = RecipeForm()

    return render(request, "create.html", {"form": form})


@login_required(login_url='/login/')
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    comments = recipe.comments.all().order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = recipe
            comment.user = request.user
            comment.save()
            messages.success(request, "Комментарий добавлен!")
            return redirect('recipe_detail', pk=pk)
        else:
            messages.error(request, "Проверьте поля формы.")
    else:
        form = CommentForm()

    context = {
        'recipe': recipe,
        'comments': comments,
        'comment_form': form,
    }
    return render(request, 'detail.html', context)


@login_required
def recipe_update(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if recipe.created_by != request.user:
        messages.error(request, "Вы не можете редактировать чужой рецепт.")
        return redirect('recipe_detail', pk=pk)

    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, "Рецепт успешно обновлён!")
            return redirect('recipe_detail', pk=pk)
        else:
            messages.error(request, "Проверьте поля формы.")
    else:
        form = RecipeForm(instance=recipe)

    return render(request, "update.html", {"form": form, "recipe": recipe})


@login_required
@require_http_methods(["GET", "POST"])
def recipe_delete(request, pk):
    # Только рецепт, который принадлежит текущему пользователю
    recipe = get_object_or_404(Recipe, pk=pk, created_by=request.user)

    if request.method == "POST":
        recipe_title = recipe.title  # сохраняем для сообщения
        recipe.delete()
        messages.success(request, f"Рецепт «{recipe_title}» успешно удалён!")
        return redirect("recipe_list")

    # GET → показываем подтверждение удаления
    return render(request, "list.html", {
        "recipe_to_delete": recipe,
        # желательно добавить:
        # "recipe_title": recipe.title,
        # "cancel_url": request.META.get("HTTP_REFERER", "recipe_list"),
    })