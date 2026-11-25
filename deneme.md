# Database Design — StudySpace

**Belge sürümü:** 0.1  
**Durum:** Taslak — onay bekliyor  
**Veritabanı:** SQLite

## 1. Amaç

Bu belge, StudySpace uygulamasında kullanılacak veritabanı yapısını tanımlar.

Veritabanı aşağıdaki bilgileri saklayacaktır:

- Kullanıcı hesapları ve rolleri
- Kütüphane katları ve çalışma masaları
- Masa kullanım oturumları

Veritabanı tasarımında gereksiz karmaşıklıktan kaçınılacak ve ilk sürümün ihtiyaçları esas alınacaktır.

## 2. Tablolar

İlk sürümde dört tablo kullanılacaktır:

1. `users`
2. `floors`
3. `seats`
4. `sessions`

### 2.1. `users` — Kullanıcılar

Kayıtlı öğrencileri ve yöneticileri tutar.

| Alan | Veri tipi | Açıklama |
|---|---|---|
| `id` | INTEGER | Birincil anahtar |
| `name` | TEXT | Kullanıcının görünen adı |
| `email` | TEXT | E-posta adresi, benzersiz |
| `password_hash` | TEXT | Parolanın güvenli özeti |
| `role` | TEXT | `student` veya `admin` |
| `created_at` | TEXT | Hesabın oluşturulma zamanı |

Kurallar:

- Her kullanıcının benzersiz bir `id` değeri olacaktır.
- E-posta adresi tekrar edemeyecektir.
- Parolalar açık metin olarak saklanmayacaktır.
- Yeni kullanıcıların rolü varsayılan olarak `student` olacaktır.
- Yönetici yetkisi normal kayıt işlemiyle kazanılamayacaktır.

### 2.2. `floors` — Katlar

Kütüphanedeki katları tanımlar.

| Alan | Veri tipi | Açıklama |
|---|---|---|
| `id` | INTEGER | Birincil anahtar |
| `name` | TEXT | Kat adı, ör. `1. Kat` |

İlk sürümde her masa yalnızca bir kata bağlı olacaktır.

### 2.3. `seats` — Masalar

Kullanılabilir çalışma alanlarını tanımlar. Buradaki `seat` terimi, tek bir sandalye yerine sistemde seçilebilir bir çalışma yerini ifade eder; istersek birden fazla sandalyeli masaları da bu şekilde modelleyebiliriz.

| Alan | Veri tipi | Açıklama |
|---|---|---|
| `id` | INTEGER | Birincil anahtar |
| `floor_id` | INTEGER | İlgili katın kimliği |
| `label` | TEXT | Masa kodu, ör. `A-01` |
| `has_power` | INTEGER | Priz var mı? `0` veya `1` |
| `qr_token` | TEXT | QR kodunda kullanılacak benzersiz tanımlayıcı |
| `is_active` | INTEGER | Masa kullanım için açık mı? |

Kurallar:

- Her masa bir kata bağlı olacaktır.
- `label`, aynı kat içinde benzersiz olacaktır.
- QR tanımlayıcısı benzersiz olacaktır.
- Bir masa devre dışı bırakıldığında geçmiş oturum kayıtları silinmeyecektir.
- Masanın dolu veya boş olması ayrıca elle yazılmayacaktır; aktif oturumlar üzerinden hesaplanacaktır.

### 2.4. `sessions` — Kullanım oturumları

Bir öğrencinin bir masayı hangi zaman aralığında kullandığını tutar.

| Alan | Veri tipi | Açıklama |
|---|---|---|
| `id` | INTEGER | Birincil anahtar |
| `user_id` | INTEGER | Oturumu başlatan kullanıcı |
| `seat_id` | INTEGER | Kullanılan masa |
| `started_at` | TEXT | Başlangıç zamanı |
| `ended_at` | TEXT | Bitiş zamanı; aktif oturumda boş |
| `status` | TEXT | `active`, `completed` veya `expired` |
| `end_reason` | TEXT | Oturumun kapanma nedeni |

`user_id` ve `seat_id`, sırasıyla `users.id` ve `seats.id` alanlarına yabancı anahtar olacaktır.

Kurallar:

- Bir oturum bir kullanıcıya ve bir masaya bağlı olacaktır.
- Oturum başlangıcında `status = active` olacaktır.
- Kullanıcı oturumu bitirdiğinde `status = completed` olarak güncellenecektir.
- Zaman aşımı nedeniyle kapatılan oturum `expired` olarak işaretlenecektir.
- Oturumun bitiş zamanı ve kapanma nedeni gerektiğinde raporlanabilecektir.

## 3. İlişkiler

- Bir katın birden fazla masası olabilir.
- Bir kullanıcının zaman içinde birden fazla oturumu olabilir.
- Bir masanın zaman içinde birden fazla oturumu olabilir.
- Her oturum yalnızca bir kullanıcıya ve bir masaya aittir.

## 4. Masa doluluk durumu

Masanın doluluğu `sessions` tablosundan hesaplanacaktır.

- Masayla ilişkili aktif oturum varsa masa doludur.
- Aktif oturum yoksa ve masa kullanıma açıksa masa boştur.
- `is_active = 0` olan masa kullanıma kapalıdır.

Aynı masada aynı anda iki aktif oturum oluşması engellenecektir. Aynı kullanıcının da birden fazla aktif oturum açması engellenecektir.

Bu kontroller veritabanı kısıtları ve sunucu tarafındaki işlemlerle sağlanacaktır.

## 5. Zaman ve tarih standardı

Tarih ve saatler tek bir standartta saklanacaktır. Önerilen yaklaşım UTC kullanmak ve ekranda Türkiye yerel saatine dönüştürmektir.

## 6. İlk sürümün kapsamı dışında kalan veriler

İlk sürümde aşağıdakiler veritabanında tutulmayacaktır:

- SMS veya push bildirim kayıtları
- Ceza puanları
- Fiziksel sensör verileri
- Router ve erişim noktası bağlantı kayıtları
- Ayrı bir rezervasyon sistemi

Bunlar ileride ihtiyaç duyulursa yeni tablolarla eklenebilir.

## 7. Açık kararlar

Kodlamaya başlamadan önce aşağıdaki noktalar onaylanmalıdır:

- Bir çalışma yeri tek kişilik mi olacak, yoksa bir masada birden fazla kullanıcı bulunabilecek mi?
- Kütüphanede kaç kat ve kaç masa bulunacak?
- QR kodu yalnızca masa sayfasını mı açacak, yoksa ek doğrulama da yapacak mı?
- Oturum zaman aşımı hangi koşullarda uygulanacak?
- Kullanıcı e-posta adresini doğrulamak zorunda olacak mı?

**Bu belgenin durumu:** Veritabanı yapısı önerilmiştir; açık kararlar netleştirilmeden nihai kabul edilmemiştir.