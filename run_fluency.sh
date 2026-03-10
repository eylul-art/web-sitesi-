#!/bin/bash
# 1. Eski sunucu varsa kapat
kill $(lsof -t -i:8000) 2>/dev/null

# 2. Safari'de localhost'u aç
open -a Safari http://localhost:8000

# 3. Sunucuyu başlat
echo "Fluency başlatılıyor... Kapatmak için Ctrl+C tuşlarına bas."
python3 -m http.server 8000
