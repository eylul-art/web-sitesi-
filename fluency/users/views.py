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
        # 1. KULLANICININ KAYDETTİĞİ KELİMELERİ AL (Sağ taraftaki liste için)
        # Not: Modelde tarihi updated_at olarak tuttuğumuz için ona göre sıralıyoruz
        user_words = SavedWord.objects.filter(user=request.user).order_by('-updated_at')
        context['user_words'] = user_words[:5] 
        
        # 2. KULLANICININ DERSLERİNİ AL (Menü için)
        user_langs = UserLanguageLevel.objects.filter(user=request.user)

        # 🔥 OTOMATİK DERS OLUŞTURMA: Eğer ders tablosu boşsa ama kelime kaydettiyse
        if not user_langs.exists() and user_words.exists():
            ilk_kelime = user_words.first()
            UserLanguageLevel.objects.create(
                user=request.user,
                language_code=ilk_kelime.language,
                level='A1' # Varsayılan olarak A1 atıyoruz
            )
            # Listeyi veritabanından tekrar güncelleyelim
            user_langs = UserLanguageLevel.objects.filter(user=request.user)

        context['user_languages'] = user_langs

        # 3. AKTİF DİLİ BELİRLE (Anasayfadaki Sol Kart İçin)
        active_lang_id = request.session.get('active_lang_id')
        
        if active_lang_id:
            active_lang = user_langs.filter(id=active_lang_id).first()
        else:
            # Session boşsa kullanıcının ilk dersini aktif dil yap
            active_lang = user_langs.first()
            if active_lang:
                request.session['active_lang_id'] = active_lang.id
                request.session['active_lang_code'] = active_lang.language_code

        # Değişkenleri HTML'e gönder
        context['active_lang'] = active_lang
        context['user_streak'] = 0 

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
        target_lang = 'de' 
        
    print(f"DEBUG: Test yönlendiriliyor. Dil: {target_lang}") 
    # DİKKAT: urls.py'daki değişikliğe uygun olarak start_test -> start_placement_test yapıldı
    return redirect('start_placement_test', lang_code=target_lang)