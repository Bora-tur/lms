# Network Architecture — StudySpace

**Sürüm:** 0.2  
**Durum:** Temel proje gereksinimi; uygulanacak ağ modeli  
**Önem:** Bu belge `architecture.md`, `requirements.md` ve `test-plan.md` ile birlikte okunmalıdır.

## 1. Amaç

StudySpace iki farklı erişim ihtiyacını karşılar:

1. **Herkese açık doluluk görüntüleme:** Öğrenciler kütüphaneye gelmeden internet üzerinden katları, masaları, priz durumlarını ve yaklaşık doluluğu görebilir.
2. **Kütüphane içi kullanım işlemleri:** Masa oturumu başlatma ve bitirme gibi durum değiştiren işlemler yalnızca kütüphanenin yetkili ağı üzerinden yapılabilir.

Bu ağ ayrımı projenin temel tasarım gereksinimidir; sadece gelecekte yapılabilecek bir geliştirme olarak ele alınmamalıdır.

## 2. Güvenlik hedefi

- İnternetten herkes doluluk verisini okuyabilir.
- İnternetten gelen bir istemci masa oturumu başlatamaz, bitiremez veya yönetici işlemi yapamaz.
- Kütüphane ağı üzerinden gelen istemciler, ayrıca giriş ve rol kontrolünden geçtikten sonra izin verilen işlemleri yapabilir.
- Wi-Fi bağlantısı tek başına öğrenci kimliğini kanıtlamaz; oturum açma gereklidir.
- IP adresi kontrolü tek başına kimlik doğrulama yerine geçmez.
- QR kodu masa kimliğini belirler; tek başına yetki veya fiziksel varlık kanıtı sayılmaz.

## 3. Önerilen mantıksal mimari

```text
                 INTERNET
                    |
           [Public occupancy site]
             read-only endpoints
                    |
          Published occupancy data
                    ^
                    | outbound publish/sync
                    |
             [Library LAN system]
        login + QR + start/end session
                    |
               [Core database]
                    ^
                    |
       Library Wi-Fi clients / students
```

### Public occupancy site
- Doluluk ve priz durumlarını salt okunur biçimde sunar.
- Öğrenci hesabı gerektirmeden kullanılabilir.
- Oturum başlatma/bitirme uç noktaları sunmaz.
- İç sistemin veritabanına internet üzerinden doğrudan erişmez.

### Library LAN system
- Yalnızca kütüphane ağı içinden erişilebilir olacak şekilde yapılandırılır.
- Öğrenci girişi ve yönetici rol kontrolü uygular.
- Masa oturumu başlatma/bitirme işlemlerini yapar.
- Asıl veritabanını yönetir.
- Doluluk özetini public siteye kontrollü şekilde gönderir. Önerilen yön, LAN'dan internete doğru giden bağlantıdır; internetten iç ağa yeni bir bağlantı açılmaz.

### Public verisinin güncellenmesi
- LAN sistemi doluluk özetini örneğin 30–60 saniyede bir public sisteme aktarabilir.
- Public sayfada son güncelleme zamanı gösterilir.
- Aktarım başarısız olursa public site son bilinen veriyi ve güncellik uyarısını gösterebilir.
- Aktarımın kimliği doğrulanmalı ve yalnızca gerekli doluluk alanlarını içermelidir; öğrenci e-postası veya oturum geçmişi gönderilmemelidir.

## 4. Uygulama seçenekleri

### Seçenek A — İki ayrı servis (önerilen hedef mimari)

- Public site internete açık bir sunucuda çalışır.
- LAN uygulaması kütüphane içindeki bir bilgisayarda/sunucuda çalışır.
- LAN uygulaması internet tarafına yalnızca gerekli doluluk özetini gönderir.
- LAN uygulamasına internetten doğrudan erişim açılmaz.

**Avantaj:** Ağ sınırı anlaşılır ve internetten gelen isteklerin iç işlemlere erişmesi önlenir.

**Dezavantaj:** İki servis, veri senkronizasyonu ve ayrı yapılandırma gerekir. Public ve LAN servisleri arasında SQLite dosyası ağ paylaşımıyla ortak kullanılmamalıdır.

### Seçenek B — Tek Flask uygulaması ve ağ kuralları

Tek uygulama iki tür endpoint sunar. Public endpoint'ler herkese açık; durum değiştiren endpoint'ler ise firewall/reverse proxy/ağ yapılandırmasıyla yalnızca LAN'dan erişilebilir yapılır.

**Avantaj:** Daha az uygulama kodu ve daha basit veri yönetimi.

**Dezavantaj:** Uygulama internete açıkken yanlış yapılandırılmış bir ağ kuralı iç endpoint'leri açığa çıkarabilir. Uygulama içindeki rol kontrolü ve sunucu tarafı doğrulama yine zorunludur.

Bu seçenek ancak ağı ve dağıtımı yapılandırma yetkisi varsa kullanılmalıdır. Sadece URL'yi gizlemek veya istemcinin gönderdiği bir IP başlığına güvenmek yeterli değildir.

## 5. Gerçek ağda uygulanması gereken kontroller

1. LAN uygulaması yalnızca iç ağ arayüzüne bind edilmeli veya güvenlik duvarı ile yalnızca izin verilen LAN kaynaklarından erişilebilir olmalıdır.
2. İnternetten LAN uygulamasının portlarına doğrudan erişim olmamalıdır.
3. Public servis yalnızca doluluk verisini yayımlamalıdır.
4. Öğrenci ve yönetici işlemleri sunucu tarafında kimlik ve rol kontrolü yapmalıdır.
5. `X-Forwarded-For` gibi istemci tarafından taklit edilebilecek başlıklara doğrudan güvenilmemelidir; reverse proxy kullanılıyorsa yalnızca güvenilir proxy yapılandırması kabul edilmelidir.
6. Ağ yöneticisinin izni olmadan üniversitenin router, firewall, captive portal veya erişim noktası ayarları değiştirilmemelidir.
7. Test ortamında örnek/test verileri kullanılmalıdır; gerçek öğrenci verisi gereksiz yere toplanmamalıdır.

## 6. Geliştirme ve test ortamı

İlk geliştirmede iki fiziksel sunucu gerekmeyebilir. İki Flask servisi aynı geliştirme bilgisayarında farklı portlarda çalıştırılarak işlevler test edilebilir. Ancak bu, gerçek ağ izolasyonunun kanıtı değildir.

Önerilen test aşamaları:

1. **Fonksiyon testi:** Public endpoint yalnızca doluluk özeti döndürür; LAN işlemleri doğru çalışır.
2. **Yerel erişim testi:** İki servis farklı portlarda çalışır; public serviste oturum başlatma endpoint'i bulunmadığı doğrulanır.
3. **LAN erişim testi:** İkinci bir cihaz aynı test Wi-Fi/LAN ağı üzerinden LAN servisine ulaşabilir.
4. **Dış ağ testi:** Test cihazı farklı bir ağdayken LAN servisine erişemediği doğrulanır.
5. **Yetki testi:** LAN içindeki giriş yapmamış kullanıcı oturum başlatamaz; öğrenci yönetici endpoint'lerini kullanamaz.
6. **Veri aktarım testi:** Public verinin güncellendiği, aktarım başarısızsa eski veri uyarısının gösterildiği kontrol edilir.

## 7. Kabul kriterleri

- Public doluluk sayfası giriş olmadan açılır.
- Public servis öğrenci/oturum bilgilerini yayımlamaz.
- Oturum başlatma ve bitirme yalnızca LAN uygulamasında bulunur.
- LAN uygulaması farklı bir ağdan erişilemez (gerçek ağ kurulumunda doğrulanır).
- LAN üzerinden de geçerli kullanıcı oturumu olmadan masa işlemi yapılamaz.
- Public doluluk verisinin son güncelleme zamanı görünür.
- Test raporu, yapılan erişim denemelerini ve sonuçlarını içerir.

## 8. Açık operasyonel gereksinim

Gerçek üniversite ağına kurulum için ağ yöneticisinden şu bilgilerin/izinlerin alınması gerekir:
- LAN sunucusu için kullanılabilecek cihaz ve sabit/rezervasyonlu IP
- Öğrenci Wi-Fi istemcilerinin sunucuya erişip erişemediği (client isolation olup olmadığı)
- Gerekli portlara izin verilip verilemeyeceği
- Üniversitenin internetten erişilen bir sunucu veya barındırma alanı sağlayıp sağlamadığı
- Public doluluk verisinin LAN'dan dışarı aktarılmasına izin verilip verilmediği

Bu izinler yoksa ağ mimarisi yerel test ağı üzerinde gösterilir ve gerçek üniversite ağı entegrasyonu raporda doğrulanmamış olarak açıkça belirtilir.
