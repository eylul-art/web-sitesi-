from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm

def index_view(request):
    """Ana sayfa: Kullanıcının dilini, seviyesini ve serisini çeker."""
    context = {'is_homepage': True}
    
    if request.user.is_authenticated:
        # Kullanıcının eklediği dili buluyoruz
        user_language_entry = request.user.userlanguagelevel_set.first()
        
        if user_language_entry:
            context['target_lang_code'] = user_language_entry.language_code
            lang_names = {'en': 'İngilizce', 'fr': 'Fransızca', 'de': 'Almanca', 'kr': 'Korece'}
            context['target_lang_name'] = lang_names.get(user_language_entry.language_code, user_language_entry.language_code.upper())
            
            # SEVİYE BİLGİSİNİ BURADAN GÖNDERİYORUZ
            context['user_level'] = user_language_entry.level
        else:
            context['target_lang_code'] = None
            context['target_lang_name'] = "Dil Seçilmedi"
            context['user_level'] = None

        context['user_streak'] = getattr(request.user, 'streak', 0)
        
    return render(request, 'index.html', context)

def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, "Kullanıcı adı veya şifre hatalı.")
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def profile_view(request):
    """Profil sayfası: Kullanıcının dil seviyesini gösterir."""
    user_lang = request.user.userlanguagelevel_set.first()
    context = {
        'user_lang': user_lang,
        'user_streak': getattr(request.user, 'streak', 0)
    }
    return render(request, 'users/profile.html', context)

@login_required
def dashboard_view(request):
    return render(request, 'users/dashboard.html')