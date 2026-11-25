# Requirements — StudySpace

**Sürüm:** 0.1  
**Durum:** Başlangıç kapsamı; kodlamaya başlamak için önerilen temel

## 1. Amaç

Öğrencilerin kütüphaneye gelmeden çalışma alanlarının doluluğunu ve priz durumunu görebilmesi; kütüphanede olduklarında boş bir masada kullanım oturumu başlatıp bitirebilmesi.

## 2. Kullanıcı türleri

### 2.1. Ziyaretçi
- Kayıt olmadan katların ve masaların doluluk durumunu görüntüleyebilir.
- Masa/kat bilgisi, priz durumu ve son güncelleme zamanını görebilir.
- Masa ayıramaz ve oturum başlatamaz.

### 2.2. Öğrenci
- Kayıt olabilir ve giriş yapabilir.
- Boş masaları görüntüleyebilir.
- Bir masa için oturum başlatabilir.
- Kendi aktif oturumunu ve başlangıç zamanını görebilir.
- Oturumunu bitirebilir.
- Aynı anda yalnızca bir aktif oturumu olabilir.

### 2.3. Yönetici
- Yönetici hesabıyla giriş yapabilir.
- Katları ve masaları görüntüleyebilir.
- Aktif oturumları görüntüleyebilir.
- Gerekirse bir oturumu elle sonlandırabilir.
- İlk sürümde kullanıcı/ceza yönetimi gibi kapsamlı işlevler yoktur.

## 3. İşlevsel gereksinimler

- FR-01: Ziyaretçi doluluk ekranını giriş yapmadan görüntüleyebilmelidir.
- FR-02: Doluluk ekranı yaklaşık 30–60 saniyede bir güncellenmelidir.
- FR-03: Her masa bir kata bağlı olmalıdır.
- FR-04: Her masa için priz bulunup bulunmadığı belirtilmelidir.
- FR-05: Öğrenci kayıt ve giriş yapabilmelidir.
- FR-06: Öğrenci yalnızca boş ve aktif bir masada oturum başlatabilmelidir.
- FR-07: Aynı masada aynı anda birden fazla aktif oturum bulunmamalıdır.
- FR-08: Aynı öğrencinin aynı anda birden fazla aktif oturumu bulunmamalıdır.
- FR-09: Öğrenci kendi oturumunu bitirebilmelidir.
- FR-10: Yönetici aktif oturumları görebilmeli ve gerektiğinde kapatabilmelidir.
- FR-11: Oturum başlangıç ve bitiş zamanları kaydedilmelidir.
- FR-12: QR kodu ilgili masanın sayfasını açmalıdır. İlk sürümde QR tek başına güvenli kimlik doğrulama yöntemi sayılmayacaktır.

## 4. Güvenlik ve kalite gereksinimleri

- NFR-01: Parolalar açık metin olarak saklanmamalıdır.
- NFR-02: Öğrenci, başka kullanıcıların oturumlarını değiştirememelidir.
- NFR-03: Yönetici rotaları sunucu tarafında rol kontrolü yapmalıdır.
- NFR-04: Masa durumu ve oturum oluşturma işlemleri sunucu tarafında doğrulanmalıdır.
- NFR-05: Arayüz masaüstü ve telefon ekranlarında kullanılabilir olmalıdır.
- NFR-06: Uygulama yerel geliştirme ortamında basit bir komutla çalıştırılabilmelidir.
- NFR-07: Kullanıcıdan proje için gerekmeyen kişisel veriler toplanmamalıdır.

## 5. Ağ mimarisi gereksinimi

Ağ ayrımı ilk sürümün temel tasarım gereksinimidir:
- İnternetten doluluk bilgisi salt okunur şekilde görüntülenebilmelidir.
- Masa oturumu başlatma/bitirme ve yönetici işlemleri yalnızca kütüphane LAN uygulamasında bulunmalıdır.
- Public servis iç veritabanına veya öğrenci oturum verilerine doğrudan erişmemelidir.
- LAN doluluk özetini public servise kontrollü şekilde gönderebilmelidir.
- Gerçek üniversite ağına entegrasyon için ağ yöneticisi izni gerekir. İzin yoksa iki servis yerel test ortamında ayrıştırılarak gösterilir; gerçek ağ izolasyonu yapılmış gibi iddia edilmez.

## 6. İlk sürüm kapsamı dışında

- Router/AP telemetrisinden otomatik fiziksel konum veya varlık tespiti
- Captive portal ve Wi-Fi'ye bağlanınca otomatik yönlendirme
- SMS, e-posta veya push bildirimi
- Fiziksel sensörler
- Otomatik ceza puanı
- Geleceğe yönelik masa rezervasyonu
- Üretim ortamında kurumsal ölçekli izleme ve işletim

## 7. Kabul kriterleri

İlk sürüm şu koşulları sağladığında temel prototip tamamlanmış sayılır:

1. Ziyaretçi doluluk sayfasını görebilir.
2. Öğrenci kayıt olup giriş yapabilir.
3. Öğrenci boş masada oturum başlatabilir.
4. Aynı masaya ikinci bir öğrenci aynı anda oturum başlatamaz.
5. Öğrenci kendi oturumunu bitirebilir ve masa boş görünür.
6. Yönetici aktif oturumları görüntüleyip kapatabilir.
7. Doluluk ekranı yenilendiğinde veritabanındaki güncel durumu gösterir.
8. Uygulama README'deki adımlarla başka bir geliştirici tarafından çalıştırılabilir.
9. Public doluluk endpoint'i oturum/kişisel verilerini döndürmez.
10. LAN işlem uç noktaları public servis üzerinden kullanılamaz; yerel testte ve erişim testinde bu ayrım doğrulanır.
