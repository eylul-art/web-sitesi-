from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import UserLanguageLevel
from vocabulary.models import SavedWord 

# --- KAYIT / GİRİŞ / ÇIKIŞ ---

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

# --- DASHBOARD (ANA SAYFA) ---

def index(request):
    context = {}
    if request.user.is_authenticated:
        user_level_obj = UserLanguageLevel.objects.filter(user=request.user).first()
        lang_names = {'en': 'İngilizce', 'fr': 'Fransızca', 'de': 'Almanca', 'kr': 'Korece', 'fa': 'Farsça', 'ar': 'Arapça'}
        
        if user_level_obj:
            context['target_lang_code'] = user_level_obj.language_code
            context['target_lang_name'] = lang_names.get(user_level_obj.language_code.lower(), "Dil Seçildi")
            context['user_level'] = user_level_obj.level
        else:
            context['target_lang_name'] = "Seçilmedi"
            context['user_level'] = "A1"

        # Wikipedia'dan kaydedilen son kelimeler
        context['user_words'] = SavedWord.objects.filter(user=request.user).order_by('-added_at')[:5]
    
    # EĞER HATA ALIRSAN: Burayı "index.html" olarak değiştirip dene
    return render(request, "index.html", context)

# --- PROFİL SAYFASI ---

@login_required
def profile_view(request):
    user_level_obj = UserLanguageLevel.objects.filter(user=request.user).first()
    all_words_count = SavedWord.objects.filter(user=request.user).count()
    
    lang_names = {'en': 'İngilizce', 'fr': 'Fransızca', 'de': 'Almanca', 'kr': 'Korece', 'fa': 'Farsça', 'ar': 'Arapça'}
    lang_full_name = "Dil Seçilmedi"
    
    if user_level_obj:
        lang_full_name = lang_names.get(user_level_obj.language_code.lower(), "Dil Seçilmedi")

    return render(request, "users/profile.html", {
        "user_level": user_level_obj,
        "lang_full_name": lang_full_name,
        "words_count": all_words_count
    })

# --- SEVİYE TESTİ (HATA VEREN KISIM) ---

@login_required
def placement_test(request):
    user_level_obj = UserLanguageLevel.objects.filter(user=request.user).first()
    
    # Kullanıcının dili varsa o dile, yoksa varsayılan Fransızca'ya ('fr') gönder
    lang = user_level_obj.language_code if user_level_obj else 'fr'
    
    # DİKKAT: Burada 'start_test' yazmalı, çünkü urls.py'da adı öyle!
    return redirect('start_test', lang_code=lang)