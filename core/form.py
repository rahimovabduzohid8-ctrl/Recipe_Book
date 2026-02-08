from django import forms
import core.models as models 
from core.models import CustomUser,Comment
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Foydalanuvchi nomi",
        widget=forms.TextInput(attrs={'placeholder': 'Login kiriting'})
    )
    password1 = forms.CharField(
        label="Parol",
        widget=forms.PasswordInput(attrs={'placeholder': 'Parol yarating'})
    )
    password2 = forms.CharField(
        label="Parolni tasdiqlang",
        widget=forms.PasswordInput(attrs={'placeholder': 'Parolni takrorlang'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']



class RecipeForm(forms.ModelForm):
    class Meta:
        model =models.Recipe
        fields = "__all__"



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']  
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 4,
                'cols': 15,
                'placeholder': 'Напишите ваш комментарий...',
                'class': 'form-control',  
                'required': 'required',
            }),
        }



        error_messages = {
            'text': {
                'required': 'Комментарий не может быть пустым.',
                'max_length': 'Комментарий слишком длинный.',
            }
        }

