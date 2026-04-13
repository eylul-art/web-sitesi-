import json
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Question, WritingErrorLog
from users.models import UserLanguageLevel
from django.contrib import messages

# --- DERSLERİM (ÇOKLU DİL) YÖNETİMİ ---

@login_required
def set_active_language(request, lang_id):
    """Kullanıcı dropdown'dan bir dil seçtiğinde onu aktif yapar"""
    lang = get_object_or_404(UserLanguageLevel, id=lang_id, user=request.user)
    
    # Session'a kaydediyoruz ki sitenin geri kalanı bu dili bilsin
    request.session['active_lang_id'] = lang.id
    request.session['active_lang_code'] = lang.language_code
    
    return redirect('/') # Ana sayfaya (veya dashboard'a) yönlendir

@login_required
def add_new_language(request):
    """Yeni dil seçme (kurulum) sayfasına gönderir"""
    return render(request, 'languages/select_language.html')


# --- MEVCUT TEST SİSTEMİ ---

def start_placement_test(request, lang_code):
    lang_code = lang_code.lower()
    questions = Question.objects.filter(language_code=lang_code).order_by('?')[:15]
    
    titles = {
        'de': 'Einstufungstest Deutsch',
        'en': 'English Placement Test',
        'fr': 'Test de placement de français',
        'kr': '한국어 레벨 테스트',
        'ar': 'اختبار تحديد المستوى في اللغة العربية',
        'fa': 'آزمون تعیین سطح فارسی'
    }
    
    current_title = titles.get(lang_code, f'{lang_code.upper()} Placement Test')
    
    return render(request, 'languages/test.html', {
        'questions': questions,
        'lang_code': lang_code,
        'test_title': current_title
    })

def evaluate_test(request, lang_code):
    if request.method == 'POST':
        # Sadece o dildeki soruları çek
        questions = Question.objects.filter(language_code=lang_code.lower())
        score = 0
        
        for question in questions:
            user_answer = request.POST.get(f'question_{question.id}')
            if user_answer == question.correct_answer:
                score += 1

        if score <= 3: level = 'A1'
        elif score <= 6: level = 'A2'
        elif score <= 9: level = 'B1'
        elif score <= 12: level = 'B2'
        else: level = 'C1'

        if request.user.is_authenticated:
            new_lang, created = UserLanguageLevel.objects.update_or_create(
                user=request.user,
                language_code=lang_code.lower(),
                defaults={'level': level}
            )
            # Testi bitirince o dili otomatik aktif yapalım
            request.session['active_lang_id'] = new_lang.id
            request.session['active_lang_code'] = new_lang.language_code
                
        return render(request, 'languages/result.html', {
            'lang_code': lang_code.upper(),
            'level': level,
            'score': score,
            'total': 15
        })
        
    return redirect('index')


# --- YAZMA VE DOĞRULAMA MODÜLÜ (LanguageTool) ---

@login_required
def writing_practice(request):
    """Kullanıcının metin girdiği ana sayfa (Artık Aktif Dile Göre Çalışıyor)"""
    # Önce session'da aktif bir dil var mı diye bakıyoruz, yoksa kullanıcının ilk dilini alıyoruz
    lang_code = request.session.get('active_lang_code')
    
    if not lang_code:
        user_level_obj = UserLanguageLevel.objects.filter(user=request.user).first()
        lang_code = user_level_obj.language_code if user_level_obj else 'en'
    
    lang_display = {
        'de': 'Almanca', 'en': 'İngilizce', 'fr': 'Fransızca',
        'kr': 'Korece', 'ar': 'Arapça', 'fa': 'Farsça'
    }
    
    return render(request, 'languages/writing_practice.html', {
        'target_lang_name': lang_display.get(lang_code, 'İngilizce'),
        'lang_code': lang_code
    })

@login_required
def check_writing(request):
    """LanguageTool API ile asenkron gramer kontrolü (Aktif Dile Göre)"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            text = data.get('text', '')
            
            # Yazma sayfasındaki gibi dinamik dil tespiti
            lang_code = request.session.get('active_lang_code')
            if not lang_code:
                user_level_obj = UserLanguageLevel.objects.filter(user=request.user).first()
                lang_code = user_level_obj.language_code if user_level_obj else 'en'

            # LanguageTool API Dil Kodları Eşleştirmesi
            lt_langs = {'en': 'en-US', 'de': 'de-DE', 'fr': 'fr', 'ar': 'ar', 'fa': 'fa', 'kr': 'ko'}
            target_lang = lt_langs.get(lang_code, lang_code)

            # API İsteği
            response = requests.post(
                "https://api.languagetool.org/v2/check",
                data={'text': text, 'language': target_lang}
            )
            
            results = response.json()

            # --- HATA DEFTERİNE KAYIT (LOGGING) ---
            if results.get('matches'):
                for match in results['matches']:
                    offset = match['offset']
                    length = match['length']
                    faulty_text = text[offset : offset + length]
                    
                    # Eğer modelinde alan isimleri farklıysa (örn: wrong_word) burayı modele göre güncelle
                    WritingErrorLog.objects.create(
                        user=request.user,
                        language_code=lang_code,
                        original_text=faulty_text,
                        error_message=match['message'],
                        correct_version=match['replacements'][0]['value'] if match['replacements'] else "Düzeltme önerisi yok",
                        error_type=match['rule']['category']['name']
                    )

            return JsonResponse(results)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Geçersiz İstek'}, status=405)