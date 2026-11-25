# Task Plan — StudySpace

**Ekip:** 2 kişi  
**Bütçe:** Yaklaşık 30 saat kişi başı / 60 kişi-saat  
**Amaç:** Önce küçük, çalışan sürüm; sonra iyileştirme.

## 1. İş bölümü

### Kişi A — Arayüz ve kullanıcı deneyimi
- Bootstrap temel yerleşimi ve ortak `base.html`
- Doluluk/kat ekranı
- Giriş ve kayıt sayfalarının görünümü
- Masa ayrıntısı ve aktif oturum ekranı
- Mobil görünüm ve basit JavaScript yenileme

### Kişi B — Backend ve veri modeli
- Flask uygulama iskeleti
- SQLite şeması ve başlangıç verileri
- Kayıt/giriş/çıkış
- Masa seçimi ve oturum işlemleri
- Yönetici ekranı ve yetki kontrolleri

### Ortak
- URL ve veri alanlarını başta kararlaştırma
- Birleştirme, hata düzeltme ve test
- Rapor ve sunum

Her kişi yalnızca kendi alanında çalışıp diğer kişinin kodunu görmeden ilerlememelidir; düzenli commit ve kısa entegrasyon kontrolleri yapılmalıdır.

## 2. Aşamalar

### Aşama 1 — Planı sabitleme (2–4 ekip-saat)
- Gereksinimleri gözden geçirme
- Veri modelini onaylama
- URL'leri ve dosya yapısını sabitleme

### Aşama 2 — İskelet ve veritabanı (4–6 ekip-saat)
- Flask çalışır hâle getirilir
- SQLite tabloları oluşturulur
- Örnek kat ve masa verileri eklenir
- README'deki kurulum adımları denenir

### Aşama 3 — Doluluk ekranı (6–8 ekip-saat)
- Kat/masa kartları gösterilir
- Boş/dolu ve priz bilgisi görünür
- Doluluk verisi periyodik olarak yenilenir
- Son güncelleme zamanı gösterilir

### Aşama 4 — Kimlik doğrulama ve oturumlar (12–16 ekip-saat)
- Kayıt ve giriş
- Masa oturumu başlatma
- Çift oturum engeli
- Öğrencinin oturumu bitirmesi
- Yönetici oturumları görüntüler ve kapatır

### Aşama 5 — Ağ ayrımı, test ve düzeltme (8–10 ekip-saat)
- Public doluluk servisi salt okunur çalışır
- LAN servisinde oturum işlemleri ve yönetici kontrolleri bulunur
- İlk olarak iki servis aynı geliştirme bilgisayarında farklı portlarda test edilir
- Dış ağ/LAN erişim kısıtlaması için hedef dağıtım ve gerekli izinler belgelenir
- Aynı masaya iki kullanıcı erişmeye çalışır
- Yetkisiz kullanıcı korumalı rotayı açmayı dener
- Oturum başlatma/bitirme doğrulanır
- Telefon ve masaüstünde arayüz denenir

### Aşama 6 — Rapor ve sunum (8–10 ekip-saat)
- Mimari ve veritabanı anlatımı
- Ekran görüntüleri
- Test sonuçları
- Demo senaryosu

Bu süreler tahmindir; toplamı hedef bütçeyi aşarsa QR ve yönetici arayüzünün görsel iyileştirmeleri gibi ikincil işleri azaltın.

## 3. Öncelik sırası

**P0 — Teslim için zorunlu**
- Doluluk ekranı
- Kayıt/giriş
- Masa oturumu başlatma/bitirme
- Aynı masanın iki kez alınmasını önleme
- Temel yönetici işlemi
- Kurulum README'si

**P1 — Zaman kalırsa**
- QR kodları
- Son güncelleme etiketi ve filtreler
- Görsel iyileştirmeler

**P2 — Sonraki sürüm**
- Gerçek üniversite ağına kurulum ve ağ yöneticisi gerektiren firewall/captive portal değişiklikleri
- Wi-Fi bağlantı takibi
- Bildirimler ve ceza sistemi
- Sensörler

## 4. Çalışma protokolü

- Her görev küçük ve test edilebilir olmalıdır.
- Her özellikten sonra uygulama çalıştırılır.
- Değişiklikler Git commit'leriyle kaydedilir.
- Bir kişi ortak arayüz veya veritabanı şemasını değiştirecekse önce diğer kişiye haber verir.
- AI tarafından üretilen kod okunmadan ve test edilmeden tamamlanmış sayılmaz.
