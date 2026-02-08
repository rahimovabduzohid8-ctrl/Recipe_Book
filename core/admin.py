from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import CustomUser,Recipe,Comment
# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display=("title",)
    search_fields=("title","description")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=("user","text")