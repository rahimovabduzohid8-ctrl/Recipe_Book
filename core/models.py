from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
ROLE=(
    ("client","Client"),
    ("admin","Admin")
)
    

class CustomUser(AbstractUser):
    role=models.CharField(max_length=100, choices=ROLE)

    def __str__(self):
        return self.username

class Recipe(models.Model):
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=200)
    image=models.ImageField(upload_to="images/")
    created_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def is_liked_by(self, user):
        if not user.is_authenticated:
            return False
        return self.likes.filter(user=user).exists()
    
    def __str__(self):
        return self.title
    
    
class Like(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_recipe_user_like'
            )
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} yoqtirdi → {self.recipe}"



class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user}: {self.text[:50]} → {self.recipe}"

