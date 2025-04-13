# Eğitim ve Danışmanlık Platformu

Bu platform, kullanıcıların eğitim hedeflerine yönelik kişiselleştirilmiş danışmanlık alabileceği, içerik paylaşabileceği ve toplulukla etkileşim kurabileceği web tabanlı bir sistemdir.

## Özellikler

- Not Paylaşımı: Kullanıcılar çeşitli dersler ve konularla ilgili notlarını paylaşabilir
- Sohbet Odaları: Discord benzeri odalarda kullanıcılar arası iletişim
- Kullanıcı Yönetimi: Kayıt, giriş ve profil yönetimi

## Teknik Altyapı

- Django 4.2+
- Django REST Framework
- Channels (WebSocket desteği)
- PostgreSQL

## Kurulum

1. Sanal ortam oluşturun ve aktif edin
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

2. Gereksinimleri yükleyin
```bash
pip install -r requirements.txt
```

3. Veritabanı migrasyonlarını yapın
```bash
python manage.py migrate
```

4. Geliştirme sunucusunu başlatın
```bash
python manage.py runserver
```

## Proje Yapısı

Proje modüler bir yapıda tasarlanmıştır:

- `accounts`: Kullanıcı yönetimi
- `notes`: Not paylaşım sistemi
- `chat`: Gerçek zamanlı sohbet sistemi