from django import forms

from django.contrib.auth.forms import AuthenticationForm



class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя",
        widget=forms.TextInput(attrs={'placeholder': 'Логин'}))

    password = forms.CharField(label="Пароль",
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))

