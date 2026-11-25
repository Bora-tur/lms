# Decision Log — StudySpace

Bu dosya alınan teknik ve kapsam kararlarının kaydını tutar. Yeni kararlar eklendiğinde tarih ve gerekçe belirtilmelidir.

## D-001 — Teknoloji yığını
**Durum:** Önerildi  
**Karar:** Python, Flask, SQLite, HTML, Bootstrap 5 ve gerektiğinde vanilla JavaScript.  
**Gerekçe:** Küçük ekip için düşük kurulum ve entegrasyon maliyeti.

## D-002 — Public ve LAN servislerinin ayrılması
**Durum:** Hedef mimari olarak önerildi  
**Karar:** Public doluluk servisi ve LAN oturum servisi ayrı mantıksal servisler olacaktır. LAN servisi doluluk özetini public servise kontrollü olarak aktaracaktır.  
**Gerekçe:** İnternetten iç oturum işlemlerine doğrudan erişimi önlemek ve veri paylaşımını salt okunur tutmak. İlk prototipte iki servis aynı bilgisayarda farklı portlarda çalıştırılabilir; gerçek ağ izolasyonu ayrıca doğrulanmalıdır.

## D-003 — Rezervasyon yerine kullanım oturumu
**Durum:** Önerildi  
**Karar:** Gelecekteki zaman dilimleri için rezervasyon yapılmayacak. Öğrenci geldiğinde boş masada oturum başlatacaktır.  
**Gerekçe:** Kapsamı ve kötüye kullanım riskini azaltmak.

## D-004 — Doluluk hesabı
**Durum:** Önerildi  
**Karar:** Doluluk, aktif oturumdan türetilecektir.  
**Gerekçe:** Masa durumunun oturum verisiyle çelişmesini önlemek.

## D-005 — Wi-Fi takibi
**Durum:** İlk sürüm dışında  
**Karar:** Router/AP entegrasyonu, captive portal ve gerçek bağlantı takibi ilk sürümde yapılmayacaktır.  
**Gerekçe:** Ağ yöneticisi erişimi ve ek entegrasyon gereksinimleri.

## D-006 — QR kodu
**Durum:** Önerildi  
**Karar:** QR kodu ilgili masa sayfasını açacaktır; QR tek başına kimlik doğrulama veya fiziksel varlık kanıtı değildir.  
**Gerekçe:** Basit prototipte yeterli, güvenlik iddiası sınırlı.

## Karar değiştirme kuralı
Kapsamı veya şemayı etkileyen bir değişiklik yapılmadan önce:
1. Gerekçe yazılır.
2. Etkilenen belgeler belirlenir.
3. İki geliştirici anlaşır.
4. İlgili belgeler güncellenir.
5. Sonra kod değiştirilir.

## D-007 — Ağ ayrımı temel gereksinimdir
**Durum:** Önerildi  
**Karar:** İnternetten yalnızca doluluk verisi görüntülenir; masa işlemleri kütüphane LAN servisi üzerinden yapılır.  
**Gerekçe:** Kullanıcının temel proje hedefi. Bu özellik kapsam dışı değildir. Gerçek üniversite ağına kurulum için yetkili ağ yöneticisi gerekir.
