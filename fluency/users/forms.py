from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from languages.models import Language, Level

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="Ad")
    last_name = forms.CharField(max_length=30, required=True, label="Soyad")
    email = forms.EmailField(required=True, label="Email Adresi")
    
    target_language = forms.ModelChoiceField(
        queryset=Language.objects.all(), 
        label="Öğrenmek İstediğim Dil",
        empty_label="Dil Seçiniz",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    target_level = forms.ModelChoiceField(
        queryset=Level.objects.all(), 
        label="Mevcut Seviyem",
        empty_label="Seviye Seçiniz",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'target_language', 'target_level')

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Email veya Kullanıcı Adı", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Şifre", widget=forms.PasswordInput(attrs={'class': 'form-control'}))