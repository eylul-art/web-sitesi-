from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm

def index_view(request):
    """Ana sayfa: Giriş yapmış kullanıcıyı Dashboard'a yönlendirebilir 
    veya giriş yapmamış kişiye Landing Page gösterir."""
    context = {
        'is_homepage': True,
    }
    if request.user.is_authenticated:
        # İleride veritabanından çekilecek örnek veriler
        context['user_streak'] = 5
        context['xp_points'] = 1250
        # Giriş yapan kullanıcıyı direkt Dashboard içeriğiyle karşılamak için 
        # index.html içinde {% if user.is_authenticated %} kontrolü kullanıyoruz.
        
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
    """Kullanıcının profil bilgilerini gördüğü yer."""
    return render(request, 'users/profile.html')

@login_required
def dashboard_view(request):
    """Derslerin, kelimelerin ve dil seçimlerinin olduğu ana panel."""
    # Burada veritabanından dersleri çekip gönderebilirsin
    # Örn: courses = Course.objects.all()
    return render(request, 'users/dashboard.html')