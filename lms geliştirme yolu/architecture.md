# Architecture — StudySpace

**Sürüm:** 0.1

## 1. Mimari hedef

İki kişilik bir ekibin kısa sürede geliştirebileceği, kolay çalıştırılabilir ve anlaşılır bir monolitik Flask uygulaması oluşturmak.

## 2. Teknoloji yığını

- Python 3
- Flask
- SQLite (`sqlite3`)
- HTML templates (Jinja)
- Bootstrap 5
- Vanilla JavaScript
- Git/GitHub

Ek frontend framework'ü, ayrı API sunucusu veya Docker ilk sürüm için gerekli değildir.

## 3. Mantıksal bileşenler

- **Public pages:** Doluluk ekranı ve kat/masa bilgileri.
- **Authentication:** Kayıt, giriş, çıkış ve kullanıcı oturumu.
- **Student functions:** Masa görüntüleme, oturum başlatma ve bitirme.
- **Admin functions:** Aktif oturumları görüntüleme ve kapatma.
- **Database layer:** SQLite sorguları ve veri tutarlılığı.
- **Templates/static:** HTML, CSS, JavaScript ve simgeler.

## 4. Önerilen URL'ler

| Method | Path | Erişim | Amaç |
|---|---|---|---|
| GET | `/` | Herkes | Doluluk ekranı |
| GET | `/api/occupancy` | Herkes | Doluluk verisini JSON olarak sunma |
| GET/POST | `/register` | Ziyaretçi | Kayıt |
| GET/POST | `/login` | Ziyaretçi | Giriş |
| POST | `/logout` | Giriş yapan | Çıkış |
| GET | `/seats/<id>` | Herkes | Masa ayrıntısı |
| POST | `/seats/<id>/start` | Öğrenci | Oturum başlatma |
| GET | `/my-session` | Öğrenci | Aktif oturumu görüntüleme |
| POST | `/sessions/<id>/end` | Oturum sahibi | Oturumu bitirme |
| GET | `/admin` | Yönetici | Yönetici paneli |
| POST | `/admin/sessions/<id>/end` | Yönetici | Oturumu elle bitirme |

Durum değiştiren işlemler GET yerine POST kullanmalıdır.

## 5. İnternet ve LAN ayrımı

Ağ ayrımı temel gereksinimdir. İnternetten yalnızca doluluk özeti okunabilmeli; oturum başlatma/bitirme ve yönetici işlemleri yalnızca kütüphane LAN uygulamasından yapılmalıdır.

Önerilen hedef mimari iki mantıksal servistir:
- Public occupancy service: salt okunur doluluk verisi sunar.
- Library LAN service: kimlik doğrulama, QR, masa oturumları ve yönetici işlemlerini yönetir.

LAN servisi, gerekli doluluk özetini public servise dışarı doğru kontrollü biçimde aktarır. Public servis iç veritabanına doğrudan erişmez. Ayrıntılı mimari, ağ kuralları ve testler için [`network-architecture.md`](network-architecture.md) belgesine bakın.

İlk geliştirme testlerinde servisler aynı bilgisayarda farklı portlarda çalıştırılabilir. Bu yalnızca işlevsel prototiptir; gerçek LAN izolasyonunu kanıtlamaz. Gerçek ağ testi için LAN ve dış ağdan erişim ayrı ayrı denenmelidir.

## 6. Güvenlik kuralları

- `SECRET_KEY` kaynak koduna sabitlenmemeli; ortam değişkeninden alınmalıdır.
- Parolalar güvenli şekilde hash'lenmelidir.
- Her korumalı rota kullanıcı ve rol kontrolü yapmalıdır.
- Formlarda CSRF koruması kullanılmalıdır.
- Veritabanı sorguları parametreli olmalıdır.
- Kullanıcı girdileri doğrulanmalıdır.
- Geliştirme sunucusu üretim ortamında kullanılmamalıdır.

## 7. Önerilen dosya yapısı

```text
studyspace/
├── app.py
├── db.py
├── schema.sql
├── requirements.txt
├── README.md
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── seat_detail.html
│   ├── my_session.html
│   └── admin.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── occupancy.js
```

Bu başlangıç yapısı gerektiğinde sadeleştirilebilir; ancak kodlama başladıktan sonra dosyaları gerekçesiz yere yeniden adlandırmaktan kaçınılmalıdır.
