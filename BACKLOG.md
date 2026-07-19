# Product Backlog — Media Mirror

Tek geliştirici, tek sprint gerçeğine göre önceliklendirilmiştir. Son sprint: **20 Temmuz – 2 Ağustos 2026**, ürün teslimi **2 Ağustos 23:59**.

Öncelik anahtarı:
- **P0** — MVP bunsuz teslim edilemez
- **P1** — MVP'nin değerini/puanını belirgin artırır, hedeflenen kapsamda
- **P2** — Zaman kalırsa (stretch)

## Puanlama Mantığı (Story Points)
- Tahminler Fibonacci ölçeğiyle yapılır (1, 2, 3, 5, 8, 13); puan, işin karmaşıklığını ve belirsizliğini temsil eder.
- Geliştirme story'lerinin toplamı **76 puandır**. Tek geliştirici olduğu için sprint kapasitesi klasik takım hızıyla değil, kalan süreye göre planlanmıştır.
- Dağılım: **Sprint 1** planlama/dokümantasyon sprintiydi (story point'siz işler: ürün tanımı, backlog, repo kurulumu, TMDb erişimi). **Sprint 2** hedefi kapsamın netleştirilmesi + MVP çekirdeği (#1–#11, #13 = **71 puan**) — tamamlandı. **Sprint 3** hedefi kalan **5 puan** (#12) + test/cila, video ve teslim setidir.
- En büyük tekil story (13 puan), toplamın yarısından küçük tutulmuştur; 13'ten büyük çıkan tahminler story bölünerek küçültülmüştür.

## User Story'ler

| # | Öncelik | Puan | User Story | Kabul Kriteri | Puan eşleşmesi |
|---|---|---|---|---|---|
| 1 | P0 | 5 | İzleyici olarak bir film/dizi adı yazıp analiz başlatmak istiyorum | Türkçe veya orijinal başlıkla arama çalışır; yapım TMDb'de bulunur | Fonksiyonel Yeterlilik |
| 2 | P0 | 3 | Aramam birden fazla yapımla eşleştiğinde doğru olanı seçmek istiyorum | Poster + yıl bilgisiyle seçim listesi gösterilir; seçim analizle devam eder | Kullanıcı Değeri |
| 3 | P0 | 5 | Veri Agent'ın yapımı doğrulayıp karakter listesini hazırlamasını istiyorum | TMDb'den karakter/oyuncu listesi çekilir, analiz bağlamı üretilir | YZ Öğeleri, Agent/orkestrasyon |
| 4 | P0 | 13 | Feminist Analiz Agent'ın kadın karakterleri tek tek analiz etmesini istiyorum | Her kadın karakter için konum + ajans + klişe değerlendirmesi üretilir | YZ Öğeleri (35p'nin çekirdeği) |
| 5 | P0 | 8 | Rapor Agent'ın sonucu sabit şablonlu Türkçe rapora derlemesini istiyorum | 4 bölümlü rapor (Genel / Karakterler / Troplar / Bulgular) her analizde aynı yapıda üretilir | Ürün Bütünlüğü |
| 6 | P0 | 8 | Raporu sade bir web arayüzünde görmek istiyorum | Streamlit: giriş alanı → seçim → rapor akışı uçtan uca çalışır | Fonksiyonel Yeterlilik |
| 7 | P1 | 8 | Eleştirmen Agent'ın raporu denetlemesini istiyorum | Tutarlılık/halüsinasyon denetimi çalışır; sorun bulursa en fazla 1 düzeltme turu döner | Agent/hafıza/orkestrasyon (15p) |
| 8 | P1 | 3 | Model yapımı tanımıyorsa uydurma yerine dürüst bir mesaj almak istiyorum | Az bilinen yapımlarda "güvenilir analiz üretemiyorum" yanıtı döner | Ürün Bütünlüğü, YZ Öğeleri |
| 9 | P1 | 2 | Kadın karakteri olmayan yapımlarda bunun bulgu olarak raporlanmasını istiyorum | Boş sonuç yerine "temsil yokluğu" raporu üretilir | İhtiyaç-Çözüm Eşleşmesi |
| 10 | P1 | 5 | Geçmiş analizlerime dönebilmek istiyorum | Analizler SQLite'a kaydedilir; arayüzde "Geçmiş Analizler" listesi çalışır | Hafıza (15p kalemi) |
| 11 | P1 | 3 | Aynı yapımı tekrar sorguladığımda sonucu beklemeden almak istiyorum | Önbellekten anında dönüş; API çağrısı tekrarlanmaz | Hafıza, Kullanıcı Değeri |
| 12 | P1 | 5 | Ürünü canlı bir linkten kullanmak istiyorum | Streamlit Community Cloud'da yayında; anahtarlar secrets'ta | Canlıya alma (10p) |
| 13 | P2 | 8 | Raporu paylaşılabilir kısa bir özet kart olarak da görmek istiyorum | Rapor sonunda tek görsellik özet kart üretilir | Kullanıcı Değeri |
| 14 | P2 | — | (Roadmap) Dizilerde sezon seçebilmek istiyorum | — kapsam dışı, roadmap kaydı | — |

## Sprint 3 Günlük Planı (20 Temmuz – 2 Ağustos)

| Günler | Hedef | Story'ler |
|---|---|---|
| 20–21 Tem | Repo + iskelet: proje yapısı, TMDb servisi, arama + seçtirme | #1, #2 |
| 22–24 Tem | Çekirdek pipeline: Veri → Analiz → Rapor agent'ları, prompt tasarımı | #3, #4, #5 |
| 25–26 Tem | Eleştirmen Agent + dürüstlük koruması + kenar durumlar | #7, #8, #9 |
| 27–28 Tem | Streamlit arayüzü uçtan uca + hafıza/arşiv/önbellek | #6, #10, #11 |
| 29 Tem | Deployment (Streamlit Community Cloud) | #12 |
| 30 Tem | Farklı yapımlarla test (bilinen film, dizi, az bilinen yapım, kadınsız yapım), cila | tümü |
| 31 Tem | 3 dk tanıtım videosu çekimi + YouTube; sprint belgelerinin tamamlanması | teslim seti |
| 1–2 Ağu | Tampon: kalan pürüzler, README son kontrol, **teslim formu (2 Ağu 23:59)** | teslim |

## Teslim Kontrol Listesi (2 Ağustos 23:59)
- [ ] Public GitHub reposu güncel (kod + tüm belgeler)
- [ ] Sprint 1-2-3 raporları ve kanıtları repoda
- [ ] Canlı ürün linki çalışıyor
- [ ] 3 dakikalık proje videosu YouTube'da
- [ ] Ürün Teslim Formu eksiksiz gönderildi
