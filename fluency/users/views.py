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
    lang_names = {
        'en': 'İngilizce', 'fr': 'Fransızca', 'de': 'Almanca', 
        'kr': 'Korece', 'fa': 'Farsça', 'ar': 'Arapça'
    }

    if request.user.is_authenticated:
        # Kullanıcının dil seviyesi objesini alıyoruz
        user_level_obj = UserLanguageLevel.objects.filter(user=request.user).first()
        
        if user_level_obj and user_level_obj.language_code:
            # Kullanıcının GERÇEK seçimi (Küçük harfe zorla: 'de', 'fr' vb.)
            current_lang = user_level_obj.language_code.lower()
            context['target_lang_code'] = current_lang
            context['target_lang_name'] = lang_names.get(current_lang, "Dil Seçildi")
            context['user_level'] = user_level_obj.level
        else:
            # Eğer kullanıcı hiç dil seçmediyse, boş bırakalım ki arayüzde 'Dil Seç' uyarısı çıksın
            # Veya senin istediğin gibi güvenli bir varsayılan (Örn: 'de')
            context['target_lang_code'] = None 
            context['target_lang_name'] = "Seçilmedi"
            context['user_level'] = "A1"

        # Wikipedia'dan kaydedilen kelimeler (Kullanıcıya özel)
        context['user_words'] = SavedWord.objects.filter(user=request.user).order_by('-added_at')[:5]
    
    return render(request, "index.html", context)

# --- PROFİL SAYFASI ---

@login_required
def profile_view(request):
    user_level_obj = UserLanguageLevel.objects.filter(user=request.user).first()
    all_words_count = SavedWord.objects.filter(user=request.user).count()
    
    lang_names = {
        'en': 'İngilizce', 'fr': 'Fransızca', 'de': 'Almanca', 
        'kr': 'Korece', 'fa': 'Farsça', 'ar': 'Arapça'
    }
    
    lang_full_name = "Dil Seçilmedi"
    if user_level_obj and user_level_obj.language_code:
        lang_full_name = lang_names.get(user_level_obj.language_code.lower(), "Dil Seçilmedi")

    return render(request, "users/profile.html", {
        "user_level": user_level_obj,
        "lang_full_name": lang_full_name,
        "words_count": all_words_count
    })

# --- SEVİYE TESTİ YÖNLENDİRME ---

@login_required
def placement_test(request):
    # 1. Önce kullanıcının dilini bulmaya çalış
    user_level = UserLanguageLevel.objects.filter(user=request.user).first()
    
    # 2. Eğer dil seçiliyse o dile, seçili değilse 'de' (Almanca) testine zorla gönder
    if user_level and user_level.language_code:
        target_lang = user_level.language_code.lower()
    else:
        target_lang = 'de' # Burayı 'de' yaptım çünkü Almanca istiyordun
        
    print(f"DEBUG: Test yönlendiriliyor. Dil: {target_lang}") # Terminalde gör diye
    return redirect('start_test', lang_code=target_lang)