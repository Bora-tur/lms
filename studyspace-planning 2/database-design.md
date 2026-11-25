# Database Design — StudySpace

**Sürüm:** 0.1  
**Durum:** Uygulama öncesi taslak  
**Veritabanı:** SQLite

## 1. Tasarım ilkeleri

- İlk sürüm için basit ve ilişkisel bir model kullanılacaktır.
- Masa doluluğu, `seats` tablosuna ayrıca yazılmak yerine aktif oturumdan türetilecektir.
- Silmek yerine gerektiğinde kaydı devre dışı bırakma tercih edilecektir.
- Zaman damgaları UTC olarak saklanacak, arayüzde yerel saate dönüştürülecektir.

## 2. Tablolar

### 2.1. `users`

| Alan | Tür | Kurallar / açıklama |
|---|---|---|
| `id` | INTEGER | Primary key |
| `name` | TEXT | Not null |
| `email` | TEXT | Not null, unique |
| `password_hash` | TEXT | Not null |
| `role` | TEXT | `student` veya `admin`; varsayılan `student` |
| `created_at` | TEXT | Not null |

### 2.2. `floors`

| Alan | Tür | Kurallar / açıklama |
|---|---|---|
| `id` | INTEGER | Primary key |
| `name` | TEXT | Not null, unique |

### 2.3. `seats`

| Alan | Tür | Kurallar / açıklama |
|---|---|---|
| `id` | INTEGER | Primary key |
| `floor_id` | INTEGER | Foreign key → `floors.id` |
| `label` | TEXT | Not null; aynı kat içinde benzersiz |
| `has_power` | INTEGER | `0` veya `1` |
| `qr_token` | TEXT | Unique; ilk sürümde rastgele ve tahmin edilmesi zor değer |
| `is_active` | INTEGER | `0` veya `1`, varsayılan `1` |

### 2.4. `sessions`

| Alan | Tür | Kurallar / açıklama |
|---|---|---|
| `id` | INTEGER | Primary key |
| `user_id` | INTEGER | Foreign key → `users.id` |
| `seat_id` | INTEGER | Foreign key → `seats.id` |
| `started_at` | TEXT | Not null |
| `ended_at` | TEXT | Aktif oturumda null |
| `status` | TEXT | `active`, `completed` veya `expired` |
| `end_reason` | TEXT | Örn. `user_ended`, `admin_ended`, `timeout`; boş olabilir |

## 3. İlişkiler

- `floors` 1 → N `seats`
- `users` 1 → N `sessions`
- `seats` 1 → N `sessions`

## 4. Doluluk kuralları

- `status = 'active'` olan oturumu bulunan masa doludur.
- Aktif oturumu olmayan ve `is_active = 1` olan masa boştur.
- `is_active = 0` olan masa kullanıma kapalıdır.

Aynı masada ve aynı kullanıcıda birden fazla aktif oturum engellenmelidir. SQLite üzerinde uygun partial unique index'ler kullanılabilir:

- `sessions(seat_id)` için `status = 'active'` koşullu benzersiz indeks
- `sessions(user_id)` için `status = 'active'` koşullu benzersiz indeks

Oturum oluşturma işlemi transaction içinde yapılmalı ve masa durumu sunucu tarafında yeniden kontrol edilmelidir.

## 5. Güvenlik

- Parola hiçbir zaman açık metin saklanmaz; Flask'ın güvenli parola hash mekanizması kullanılır.
- Öğrenci yalnızca kendi oturumunu kapatabilir.
- Yönetici işlemleri sunucu tarafında rol kontrolünden geçer.
- QR kodu bir masayı tanımlar; tek başına oturum yetkisi vermez.

## 6. İlk sürüm dışında

Bildirimler, ceza puanları, sensör verileri, Wi-Fi bağlantı kayıtları ve ileri rezervasyonlar için tablo oluşturulmayacaktır.

## 7. Açık kararlar

- Çalışma yeri tek kişi için mi tanımlanacak? İlk sürüm varsayımı: evet.
- E-posta doğrulaması gerekiyor mu? İlk sürüm varsayımı: hayır.
- Oturum zaman aşımı uygulanacak mı? İlk sürüm varsayımı: otomatik Wi-Fi izleme yok; manuel bitirme ve yönetici kapatması var.
