# Test Plan — StudySpace

**Sürüm:** 0.1

## 1. Amaç

Temel işlevlerin, veri tutarlılığının ve rol tabanlı erişimin doğru çalıştığını doğrulamak.

## 2. Manuel test senaryoları

| ID | Senaryo | Beklenen sonuç |
|---|---|---|
| T-01 | Ziyaretçi ana sayfayı açar | Doluluk ekranı görüntülenir |
| T-02 | Geçersiz e-posta ile kayıt | Hata mesajı gösterilir |
| T-03 | Aynı e-posta ile tekrar kayıt | Kayıt reddedilir |
| T-04 | Öğrenci doğru bilgilerle giriş yapar | Öğrenci ekranına yönlendirilir |
| T-05 | Öğrenci boş masada oturum başlatır | Oturum oluşur, masa dolu görünür |
| T-06 | İkinci öğrenci aynı masayı almaya çalışır | İkinci oturum reddedilir |
| T-07 | Öğrenci kendi oturumunu bitirir | Oturum kapanır, masa boş görünür |
| T-08 | Öğrenci başka kullanıcının oturumunu kapatmayı dener | İşlem reddedilir |
| T-09 | Öğrenci yönetici sayfasını açar | Erişim reddedilir |
| T-10 | Yönetici aktif oturumu kapatır | Oturum kapanır |
| T-11 | Doluluk sayfası yenilenir | Güncel veriler görüntülenir |
| T-12 | Devre dışı masa seçilir | Oturum başlatılamaz |

## 3. Ağ ayrımı testleri

| ID | Senaryo | Beklenen sonuç |
|---|---|---|
| N-01 | İnternet/public servisine giriş yapmadan erişim | Doluluk özeti açılır |
| N-02 | Public serviste oturum başlatma endpoint'i denenir | Endpoint mevcut değildir veya işlem reddedilir |
| N-03 | Public verisi incelenir | E-posta, kullanıcı kimliği veya oturum geçmişi yayımlanmaz |
| N-04 | LAN servisinde oturum başlatma, giriş yapılmadan denenir | İşlem reddedilir |
| N-05 | Öğrenci yönetici endpoint'ini kullanır | İşlem reddedilir |
| N-06 | LAN servisine farklı ağdan erişim denenir | Gerçek dağıtımda bağlantı engellenir |
| N-07 | LAN'dan public servise doluluk özeti aktarılır | Yalnızca gerekli alanlar güncellenir |
| N-08 | Veri aktarımı başarısız olur | Public sayfa son güncelleme zamanını ve eski veri uyarısını gösterir |

İlk yerel prototipte N-06 gerçek ağ izolasyonunu doğrulamaz. Bunun için servis ayrı bir LAN cihazında/arayüzünde çalıştırılmalı ve farklı ağdan erişim denenmelidir.

## 4. Demo senaryosu

1. Ziyaretçi doluluk ekranını açar.
2. Öğrenci hesabıyla giriş yapılır.
3. Boş bir masa seçilip oturum başlatılır.
4. Doluluk ekranında masanın dolu olduğu gösterilir.
5. Öğrenci oturumu bitirir.
6. Masa tekrar boş görünür.
7. Yönetici panelinden aktif oturumları görüntüleme gösterilir.

## 5. Test ortamı

İlk aşamada yerel geliştirme ortamı kullanılacaktır. En az iki ayrı tarayıcı oturumu veya iki cihazla aynı masaya eşzamanlı erişim testi yapılmalıdır.

Gerçek üniversite Wi-Fi ağına erişim, firewall veya captive portal entegrasyonu ilk sürümün kabul testine dahil değildir.
