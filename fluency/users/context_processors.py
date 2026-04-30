# users/context_processors.py

def global_user_languages(request):
    """
    Kullanıcının dillerini tüm sayfalardaki (base.html navbarı dahil) 
    kullanıma otomatik olarak sunar.
    """
    if request.user.is_authenticated:
        # Kullanıcının eklediği tüm dilleri çekiyoruz
        languages = request.user.languages.all()
        return {'user_languages': languages}
    
    # Kullanıcı giriş yapmamışsa boş döner
    return {}