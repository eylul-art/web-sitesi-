import requests
import json
import re
import urllib.parse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SavedWord

def wiki_reader(request):
    context = {}
    db_lang_code = 'en' 
    
    if request.user.is_authenticated:
        user_lang = request.user.userlanguagelevel_set.first()
        if user_lang:
            db_lang_code = user_lang.language_code.lower()

    wiki_lang_map = {'en': 'en', 'fr': 'fr', 'de': 'de', 'kr': 'ko', 'fa': 'fa', 'ar': 'ar'}
    wiki_lang = wiki_lang_map.get(db_lang_code, 'en')

    # Arama kelimesi (q) ve seçilen makale başlığı (article)
    query = request.GET.get('q', '').strip()
    article = request.GET.get('article', '').strip()
    
    headers = {'User-Agent': 'FluencyLanguageApp/1.0 (Takim Projesi - web okuma modulu)'}
    
    # 1. SENARYO: KULLANICI LİSTEDEN BİR MAKALE SEÇTİYSE (OKUMA MODU)
    if article:
        safe_title = urllib.parse.quote(article)
        summary_url = f"https://{wiki_lang}.wikipedia.org/api/rest_v1/page/summary/{safe_title}"
        
        try:
            response = requests.get(summary_url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                context['title'] = data.get('title')
                context['content'] = data.get('extract') 
            else:
                context['error'] = "Makale yüklenemedi veya bulunamadı."
        except requests.exceptions.RequestException:
            context['error'] = "Bağlantı hatası oluştu."
            
        context['search_query'] = query # Geri dönmek isterse diye arama kelimesini tutuyoruz
        
    # 2. SENARYO: KULLANICI SADECE ARAMA YAPTIYSA (LİSTELEME MODU)
    elif query:
        safe_query = urllib.parse.quote(query)
        # Wikipedia'dan 10 tane alakalı arama sonucu istiyoruz
        search_url = f"https://{wiki_lang}.wikipedia.org/w/api.php?action=query&list=search&srsearch={safe_query}&utf8=&format=json&srlimit=10"
        
        try:
            search_response = requests.get(search_url, headers=headers, timeout=5)
            if search_response.status_code == 200:
                results = search_response.json().get('query', {}).get('search', [])
                if results:
                    context['search_results'] = results # HTML'e sonuçları gönderiyoruz
                else:
                    context['error'] = f"Maalesef '{query}' hakkında hiçbir makale bulunamadı."
            else:
                context['error'] = "Arama motoru yanıt vermiyor."
        except requests.exceptions.RequestException:
            context['error'] = "Bağlantı hatası."
            
        context['search_query'] = query

    context['lang'] = wiki_lang.upper()
    return render(request, 'vocabulary/wiki_reader.html', context)

@csrf_exempt
def save_word_ajax(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'Giriş yapmalısın!'})
        try:
            data = json.loads(request.body)
            clicked_word = data.get('word', '').strip().lower()
            lang = data.get('lang', 'en').lower()
            clean_word = re.sub(r'[^\w\s]', '', clicked_word)
            if clean_word:
                SavedWord.objects.get_or_create(user=request.user, word=clean_word, language=lang)
                return JsonResponse({'status': 'success', 'word': clean_word})
            return JsonResponse({'status': 'error', 'message': 'Geçersiz kelime.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Geçersiz istek türü.'})