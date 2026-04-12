import requests
import json
import re
import urllib.parse
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import SavedWord
from languages.models import WritingErrorLog 

def wiki_reader(request):
    """Wikipedia'dan tam HTML çeken ve akıllı arama yapan modül"""
    context = {}
    db_lang_code = 'en' 
    
    if request.user.is_authenticated:
        user_lang = request.user.userlanguagelevel_set.first()
        if user_lang:
            db_lang_code = user_lang.language_code.lower()

    wiki_lang_map = {'en': 'en', 'fr': 'fr', 'de': 'de', 'kr': 'ko', 'fa': 'fa', 'ar': 'ar'}
    wiki_lang = wiki_lang_map.get(db_lang_code, 'en')

    query = request.GET.get('q', '').strip()
    article = request.GET.get('article', '').strip()
    
    headers = {'User-Agent': 'FluencyLanguageApp/1.0 (Takim Projesi)'}
    
    if article:
        safe_title = urllib.parse.quote(article)
        parse_url = f"https://{wiki_lang}.wikipedia.org/w/api.php?action=parse&page={safe_title}&format=json&prop=text&redirects=1"
        
        try:
            response = requests.get(parse_url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'parse' in data:
                    context['title'] = data['parse']['title']
                    html_content = data['parse']['text']['*']
                    html_content = html_content.replace('src="//', 'src="https://')
                    safe_q = urllib.parse.quote(query)
                    html_content = html_content.replace('href="/wiki/', f'href="?q={safe_q}&article=')
                    context['content'] = html_content
                else:
                    context['error'] = "Makale içeriği alınamadı."
            else:
                context['error'] = "Makale yüklenemedi veya bulunamadı."
        except requests.exceptions.RequestException:
            context['error'] = "Bağlantı hatası oluştu."
            
        context['search_query'] = query 
        
    elif query:
        safe_query = urllib.parse.quote(query)
        search_url = f"https://{wiki_lang}.wikipedia.org/w/api.php?action=query&list=search&srsearch={safe_query}&utf8=&format=json&srlimit=10"
        
        try:
            search_response = requests.get(search_url, headers=headers, timeout=5)
            if search_response.status_code == 200:
                results = search_response.json().get('query', {}).get('search', [])
                if results:
                    context['search_results'] = results 
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
    """Tıklanan kelimeyi API ile Türkçe'ye çevirip arka planda kaydeder."""
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'Giriş yapmalısın!'})
        try:
            data = json.loads(request.body)
            clicked_word = data.get('word', '').strip().lower()
            lang = data.get('lang', 'en').lower()
            
            clean_word = re.sub(r'[^\w\s]', '', clicked_word).strip()
            
            if clean_word:
                existing_word = SavedWord.objects.filter(user=request.user, word=clean_word, language=lang).first()
                if existing_word:
                    anlam = existing_word.turkish_meaning if existing_word.turkish_meaning else "Zaten listede"
                    return JsonResponse({'status': 'info', 'word': clean_word, 'meaning': anlam, 'message': 'Zaten sözlüğünde var!'})
                
                translation = "Çeviri bulunamadı"
                try:
                    trans_url = f"https://api.mymemory.translated.net/get?q={clean_word}&langpair={lang}|tr"
                    trans_response = requests.get(trans_url, timeout=4)
                    if trans_response.status_code == 200:
                        trans_data = trans_response.json()
                        resp_data = trans_data.get('responseData')
                        if resp_data and isinstance(resp_data, dict):
                            translation = resp_data.get('translatedText', 'Çeviri bulunamadı')
                except Exception as e:
                    print("Çeviri Hatası:", e) 
                    pass 

                SavedWord.objects.create(user=request.user, word=clean_word, turkish_meaning=translation, language=lang)
                
                return JsonResponse({'status': 'success', 'word': clean_word, 'meaning': translation})
                
            return JsonResponse({'status': 'error', 'message': 'Geçersiz kelime.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Geçersiz istek türü.'})


@login_required
def my_dictionary(request):
    """Kullanıcının kaydettiği kelimeleri ve yazma hatalarını profilinde listeler."""
    words = SavedWord.objects.filter(user=request.user).order_by('-updated_at')
    writing_errors = WritingErrorLog.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'vocabulary/my_dictionary.html', {
        'words': words,
        'writing_errors': writing_errors
    })


@login_required
@csrf_exempt
def update_status(request, word_id):
    """AJAX ile kelime durumunu günceller. İsim urls.py ile eşitlendi."""
    if request.method == 'POST':
        # AJAX'tan gelen veriyi al
        new_status = request.POST.get('status')
        
        # Eğer veri body'den JSON olarak geliyorsa
        if not new_status:
            try:
                data = json.loads(request.body)
                new_status = data.get('status')
            except:
                pass

        try:
            word = SavedWord.objects.get(id=word_id, user=request.user)
            word.status = new_status
            word.save() # updated_at otomatik güncellenir
            return JsonResponse({'status': 'success', 'new_status': new_status})
        except SavedWord.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Kelime bulunamadı'}, status=404)
            
    return JsonResponse({'status': 'error', 'message': 'Geçersiz istek'}, status=400)