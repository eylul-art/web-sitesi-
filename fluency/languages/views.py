from django.shortcuts import render, redirect
from .models import Question
from users.models import UserLanguageLevel

from django.contrib import messages # Mesaj eklemek için bunu en üste ekle

# languages/views.py içinde
def start_placement_test(request, lang_code):
    lang_code = lang_code.lower()
    questions = Question.objects.filter(language_code=lang_code).order_by('?')[:15]
    
    # Başlıkları her dilin kendi dilinde tanımlayalım
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
        'test_title': current_title # Şablon için yeni başlık değişkeni
    })
def evaluate_test(request, lang_code):
    if request.method == 'POST':
        questions = Question.objects.filter(language_code=lang_code.lower())
        score = 0
        
        for question in questions:
            user_answer = request.POST.get(f'question_{question.id}')
            if user_answer == question.correct_answer:
                score += 1

        # 🔥 SENİN İSTEDİĞİN 15 SORULUK SEVİYE ARALIKLARI:
        if score <= 3:
            level = 'A1'
        elif score <= 6:
            level = 'A2'
        elif score <= 9:
            level = 'B1'
        elif score <= 12:
            level = 'B2'
        else:
            level = 'C1'

        # Kullanıcının seviyesini güncelle veya yarat
        if request.user.is_authenticated:
            user_lang, created = UserLanguageLevel.objects.update_or_create(
                user=request.user,
                language_code=lang_code.lower(),
                defaults={'level': level}
            )
                
        return render(request, 'languages/result.html', {
            'lang_code': lang_code.upper(),
            'level': level,
            'score': score,
            'total': 15 # Toplam soru sayısı
        })
        
    return redirect('index')