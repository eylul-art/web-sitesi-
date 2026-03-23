from django.shortcuts import render, redirect
from .models import Question
# Kullanıcının seviyesini kaydetmek için modelimizi çağırıyoruz
from users.models import UserLanguageLevel 

def start_placement_test(request, lang_code):
    questions = Question.objects.filter(language_code=lang_code.lower())
    if not questions.exists():
        return render(request, 'languages/no_questions.html', {'lang_code': lang_code})
    return render(request, 'languages/test.html', {
        'questions': questions,
        'lang_code': lang_code
    })

def evaluate_test(request, lang_code):
    if request.method == 'POST':
        questions = Question.objects.filter(language_code=lang_code.lower())
        score = 0
        total_questions = questions.count()
        
        # Formdan gelen cevapları kontrol et
        for question in questions:
            # HTML'de name="question_1" gibi atamıştık
            user_answer = request.POST.get(f'question_{question.id}')
            if user_answer == question.correct_answer:
                score += 1
                
        # 15 soruya göre Seviye Belirleme Algoritması
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
            
        # Eğer kullanıcı giriş yapmışsa, seviyesini veritabanına KANITLA/KAYDET!
        if request.user.is_authenticated:
            user_lang, created = UserLanguageLevel.objects.get_or_create(
                user=request.user,
                language_code=lang_code.lower(),
                defaults={'level': level}
            )
            if not created: # Eğer zaten varsa, yeni seviyeyle güncelle
                user_lang.level = level
                user_lang.save()
                
        return render(request, 'languages/result.html', {
            'lang_code': lang_code.upper(),
            'level': level,
            'score': score,
            'total': total_questions
        })
        
    # Biri URL'ye elle /evaluate/ yazıp girmeye çalışırsa ana sayfaya at
    return redirect('index')