# StudySpace — Proje Planı

**Durum:** Planlama taslağı  
**Hedef:** Kütüphane çalışma alanlarının doluluk bilgisini gösteren ve masa kullanım oturumlarını yöneten küçük, çalışan bir web prototipi.

## Belgeler

1. [`requirements.md`](requirements.md) — kapsam ve gereksinimler
2. [`user-flows.md`](user-flows.md) — öğrenci ve yönetici akışları
3. [`database-design.md`](database-design.md) — SQLite veri modeli
4. [`architecture.md`](architecture.md) — teknik mimari, sayfalar ve rotalar
5. [`task-plan.md`](task-plan.md) — geliştirme sırası ve iş bölümü
6. [`test-plan.md`](test-plan.md) — temel test senaryoları
7. [`network-architecture.md`](network-architecture.md) — public/LAN ayrımı, güvenlik ve ağ testleri
8. [`decisions.md`](decisions.md) — alınan kararlar ve ertelenen konular

## Başlangıçta sabitlenen teknoloji tercihleri

- Python + Flask
- SQLite
- HTML + Bootstrap 5 + az miktarda JavaScript
- Git ve GitHub
- Ayrı mobil uygulama yok
- İlk sürümde gerçek router/AP entegrasyonu yok

## Geliştirme ilkesi

Önce çalışan en küçük sürümü çıkarın. Her görev tamamlandığında uygulamayı çalıştırın ve ilgili testi yapın. Onaylanmış belgeleri değiştiren bir karar gerekirse önce `decisions.md` dosyasına not düşün.

## Önemli ağ gereksinimi

İnternetten doluluk görüntüleme ve yalnızca kütüphane LAN'ından oturum yönetimi projenin temel tasarım gereksinimidir. Önerilen hedef mimari iki servistir; LAN servisi doluluk özetini public servise kontrollü şekilde aktarır. Gerçek ağ izolasyonu ağ yapılandırmasıyla doğrulanmalıdır. Ayrıntılar için `network-architecture.md` dosyasına bakın.
