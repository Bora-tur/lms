# User Flows — StudySpace

**Sürüm:** 0.1

## 1. Ziyaretçi: doluluk görüntüleme

1. Ziyaretçi ana sayfayı açar.
2. Kat seçer veya tüm katları görüntüler.
3. Masaların boş/dolu ve prizli/prizsiz durumlarını görür.
4. Sayfa yaklaşık 30–60 saniyede bir güncellenir.
5. Ekranda son güncelleme zamanı gösterilir.

**Hata/istisna:** Veriler yüklenemezse kullanıcıya hata mesajı ve yeniden deneme seçeneği gösterilir.

## 2. Öğrenci: kayıt ve giriş

1. Öğrenci kayıt sayfasını açar.
2. Ad, e-posta ve parola girer.
3. Sunucu girişleri doğrular ve parolanın hash'ini kaydeder.
4. Öğrenci giriş yapar ve çalışma alanlarına yönlendirilir.

**Kurallar:** E-posta benzersiz olmalıdır. Rol kullanıcı tarafından kayıt formunda seçilemez.

## 3. Öğrenci: masa seçme ve oturum başlatma

1. Öğrenci doluluk ekranında boş bir masa görür.
2. Masaya tıklar veya o masanın QR kodunu tarayarak ilgili sayfayı açar.
3. Giriş yapmamışsa giriş sayfasına yönlendirilir; sonrasında masa sayfasına döner.
4. Öğrenci “Oturum başlat” düğmesine basar.
5. Sunucu masanın hâlâ boş ve aktif olduğunu kontrol eder.
6. Kontrol başarılıysa oturum oluşturulur ve masa dolu görünür.
7. Başka bir kullanıcı aynı anda masayı aldıysa işlem reddedilir ve güncel durum gösterilir.

## 4. Öğrenci: aktif oturum ve bitirme

1. Öğrenci aktif oturum sayfasını açar.
2. Kullanılan masa ve başlangıç zamanı gösterilir.
3. Öğrenci “Oturumu bitir” düğmesine basar.
4. Sunucu yalnızca o kullanıcıya ait aktif oturumu kapatır.
5. Masa tekrar boş görünür.

## 5. Yönetici: aktif oturumları yönetme

1. Yönetici giriş yapar.
2. Yönetici panelini açar.
3. Aktif oturumları ve ilgili masaları görüntüler.
4. Gerektiğinde bir oturumu kapatır.
5. Sistem bitiş zamanını kaydeder ve masa durumunu günceller.

## 6. İlk sürümde bağlantı kaybı

İlk sürüm Wi-Fi erişim noktası bağlantısını gerçek zamanlı izlemez. Bağlantı kaybını fiziksel ayrılış kanıtı olarak kabul etmez. Otomatik bağlantı takibi ve uyarı akışı sonraki sürüm için açık konudur.
