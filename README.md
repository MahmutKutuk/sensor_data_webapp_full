# Sensör Veri Takip ve Web Arayüzü - Full

Bu proje, pil/batarya üretim hattından gelen sensör verilerini toplamak, saklamak ve web arayüzü
üzerinden görselleştirmek için geliştirilmiş örnek bir uygulamadır.

## Nasıl çalıştırılır
1. Ortam hazırlığı:
   - Python 3.8+ yüklü olmalı
   - virtualenv kullanılması tavsiye edilir

2. Gereksinimleri yükle:
   pip install -r requirements.txt

3. Uygulamayı başlat:
   python app.py

4. Tarayıcıda aç:
   http://localhost:5000

## İçerikler
- app.py : Flask backend, örnek veritabanı oluşturur ve API endpointler sağlar.
- templates/ : Jinja2 HTML şablonları
- static/ : CSS, JS ve görseller
- data/sensor_log.csv : örnek CSV

Not: SQLite veritabanı (`sensor_data.db`) uygulama başlatıldığında otomatik oluşturulur.
