import requests

def check_grammar(text, lang_code):
    # LanguageTool API endpoint
    url = "https://api.languagetool.org/v2/check"
    
    # Bazı dil kodları LT'de farklı olabilir (örn: kr -> ko)
    lt_langs = {'en': 'en-US', 'de': 'de-DE', 'fr': 'fr', 'ar': 'ar', 'fa': 'fa', 'kr': 'ko'}
    target_lang = lt_langs.get(lang_code, lang_code)

    data = {
        'text': text,
        'language': target_lang,
    }
    
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json()
    return None