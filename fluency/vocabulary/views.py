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
    context = {}
    db_lang_code = 'en' # Varsayılan dil
    
    if request.user.is_authenticated:
        # 1. HACK: Session (Çerez) Tarayıcı! 
        # Navbar'daki buton dili nereye kaydettiyse bütün çerezleri tarayıp onu buluyoruz.
        for key, value in request.session.items():
            if 'lang' in key.lower():
                if isinstance(value, str) and len(value) <= 5: # 'de', 'fr' gibi bir kodsa
                    db_lang_code = value.lower()
                    break
                elif isinstance(value, int): # ID olarak (1, 2) kaydedildiyse
                    try:
                        lang_obj = request.user.languages.get(id=value)
                        db_lang_code = lang_obj.language_code.lower()
                        break
                    except: pass

        # 2. Eğer Session boşsa Veritabanındaki is_active alanına bak
        if db_lang_code == 'en':
            try:
                active_lang = request.user.languages.filter(is_active=True).first()
                if active_lang:
                    db_lang_code = active_lang.language_code.lower()
                else:
                    first_lang = request.user.languages.first()
                    db_lang_code = first_lang.language_code.lower() if first_lang else 'en'
            except: pass

    # 3. URL PARAMETRESİ (Sadece makale içi linklere tıklandığında çalışması için)
    url_lang = request.GET.get('lang')
    if url_lang:
        db_lang_code = url_lang.lower()

    # Wikipedia Haritası
    wiki_lang_map = {'en': 'en', 'fr': 'fr', 'de': 'de', 'kr': 'ko', 'fa': 'fa', 'ar': 'ar'}
    wiki_lang = wiki_lang_map.get(db_lang_code, 'en')

    query = request.GET.get('q', '').strip()
    article = request.GET.get('article', '').strip()
    headers = {'User-Agent': 'FluencyApp/1.0'}
    
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
                    
                    # Link tıklamalarında dilin kopmaması için:
                    safe_q = urllib.parse.quote(query)
                    html_content = html_content.replace('href="/wiki/', f'href="?lang={wiki_lang}&q={safe_q}&article=')
                    context['content'] = html_content
        except: context['error'] = "Bağlantı hatası."
            
    elif query:
        safe_query = urllib.parse.quote(query)
        search_url = f"https://{wiki_lang}.wikipedia.org/w/api.php?action=query&list=search&srsearch={safe_query}&utf8=&format=json&srlimit=10"
        try:
            search_response = requests.get(search_url, headers=headers, timeout=5)
            if search_response.status_code == 200:
                context['search_results'] = search_response.json().get('query', {}).get('search', [])
        except: context['error'] = "Arama başarısız."

    context['search_query'] = query
    context['lang'] = wiki_lang.upper() # Ekranda aslanlar gibi DE yazacak!
    return render(request, 'vocabulary/wiki_reader.html', context)


@csrf_exempt
@login_required
def save_word_ajax(request):
    """Tıklanan kelimeyi (artikeliyle birlikte) Türkçe'ye çevirir. Özel isimleri filtreler."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Frontend'den gelen orijinal kelime (Örn: "das Krankenhaus" veya "David")
            # Büyük/küçük harf kontrolü için lower() yapmıyoruz!
            original_word = data.get('word', '').strip()
            lang = data.get('lang', 'en').lower()
            
            if not original_word:
                return JsonResponse({'status': 'error', 'message': 'Geçersiz kelime.'})

            # Arama ve veritabanı kayıtları için küçük harfe çevrilmiş hali
            search_word = original_word.lower()

            # --- 1. AŞAMA: TEMEL ÖZEL İSİM KONTROLÜ ---
            # Artikelsiz geldiyse ve büyük harfle başlıyorsa
            is_capitalized = original_word[0].isupper()
            is_proper_noun = False

            if original_word.isupper(): # Tamamı büyük harfse (Örn: NATO, UNESCO)
                is_proper_noun = True
            elif lang != 'de' and is_capitalized: # İngilizce ve Fransızcada büyük harfle başlıyorsa
                is_proper_noun = True

            # Zaten sözlükte var mı?
            existing_word = SavedWord.objects.filter(user=request.user, word=search_word, language=lang).first()
            if existing_word:
                return JsonResponse({'status': 'info', 'word': search_word, 'meaning': existing_word.turkish_meaning, 'message': 'Zaten sözlüğünde!'})
            
            # --- ÇEVİRİ API'Sİ ---
            translation = search_word
            try:
                trans_url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(search_word)}&langpair={lang}|tr"
                trans_response = requests.get(trans_url, timeout=4)
                if trans_response.status_code == 200:
                    translation = trans_response.json().get('responseData', {}).get('translatedText', search_word)
            except: 
                pass 

            # --- 2. AŞAMA: GELİŞMİŞ ÖZEL İSİM KONTROLÜ ---
            # Çeviri sonucu kelimenin kendisiyle birebir aynıysa (örn: "Pink Floyd" çevrilince yine "Pink Floyd" olur)
            # ve kelime orijinalinde büyük harfle başlıyorsa (Bu kural Almancadaki özel isimleri de yakalar)
            if translation.lower() == search_word and is_capitalized:
                is_proper_noun = True

            # EĞER ÖZEL İSİMSE: Veritabanına ASLA kaydetme, sadece bilgi dön.
            if is_proper_noun:
                return JsonResponse({
                    'status': 'info', 
                    'word': original_word, 
                    'meaning': 'Özel İsim', 
                    'message': 'Özel isimler sözlüğe kaydedilmez.'
                })

            # Eğer normal bir kelimeyse sözlüğe aslanlar gibi kaydet
            SavedWord.objects.create(user=request.user, word=search_word, turkish_meaning=translation, language=lang)
            return JsonResponse({'status': 'success', 'word': search_word, 'meaning': translation})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Geçersiz istek.'})


@login_required
def my_dictionary(request):
    return render(request, 'vocabulary/my_dictionary.html', {
        'words': SavedWord.objects.filter(user=request.user).order_by('-updated_at'),
        'writing_errors': WritingErrorLog.objects.filter(user=request.user).order_by('-created_at')
    })


@login_required
@csrf_exempt
def update_status(request, word_id):
    if request.method == 'POST':
        new_status = request.POST.get('status') or json.loads(request.body).get('status')
        word = get_object_or_404(SavedWord, id=word_id, user=request.user)
        word.status = new_status
        word.save()
        return JsonResponse({'status': 'success', 'new_status': new_status})
    return JsonResponse({'status': 'error'}, status=400)