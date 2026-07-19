# Sprint 2 Raporu (6 – 19 Temmuz 2026)

## Sprint Hedefi
Ürün kapsamının tanımlanması ve proje belgelerinin (README, backlog) oluşturulması.

## Ne Yaşandı
- Sprint 1'de yazılan ilk ürün tanımı ("Media Mirror" — film karakter verilerinden **nicel** cinsiyet dağılımı + karakter ajansı çıkaran ve paylaşılabilir "farkındalık kartı" üreten araç) üzerinde çalışıldı.
- Sprint sonunda bu kapsamın iki zayıflığı görüldü:
  1. **Teknik belirsizlik:** "Karakter ajansı"nın TMDb verisinden nicel olarak çıkarılıp çıkarılamayacağı netleştirilemedi.
  2. **Vizyon uyumsuzluğu:** Asıl anlatılmak istenen şeyin sayısal bir dağılım değil, kadın karakterlerin konumuna dair **nitel, feminist bir yorum** olduğu netleşti.
- 19 Temmuz'da yapılandırılmış bir kapsam sorgulama oturumu yapıldı; ürün baştan tanımlandı.

## Alınan Kararlar (19 Temmuz kapsam oturumu)
| Konu | Karar |
|---|---|
| Çekirdek | Nicel temsil kartı → **feminist perspektiften nitel kadın karakter analizi**; dizi desteği eklendi |
| Çıktı | 4 bölümlü yapılandırılmış Türkçe rapor (Genel / Karakter Analizi / Troplar / Bulgular) |
| Veri | TMDb (doğrulama + karakter listesi) + LLM bilgisi; dürüstlük koruması ile |
| AI | Gemini API; saf Python ile el yazımı orkestrasyon (framework yok) |
| Agent'lar | Veri → Feminist Analiz → Rapor → **Eleştirmen** (max 1 düzeltme turu) |
| Hafıza | SQLite analiz arşivi + önbellek, "Geçmiş Analizler" ekranı |
| Arayüz | Streamlit; **deployment MVP kapsamında** (Community Cloud) |
| Kenar durumlar | Çoklu eşleşmede seçtirme; kadın karakter yokluğu bulgu olarak raporlanır |
| Kapsam dışı | Sezon bazlı analiz, sohbet takibi, iki dillilik → roadmap |

## Sprint Sonu Durumu
- ✅ Ürün kapsamı netleşti, README ve BACKLOG yeniden yazıldı
- ✅ Son sprint gün bazında planlandı
- ❌ Kod geliştirme başlamadı (tamamı Son Sprint'te — plan buna göre daraltıldı)

## Retrospektif
| | |
|---|---|
| **İyi giden** | Kapsam sorunları teslime 2 hafta kala fark edilip köklü biçimde çözüldü; belirsiz kısımlar (ajans ölçümü) ürüne girmeden ayıklandı |
| **Zorlayan** | Fikrin netleşmesi beklenenden uzun sürdü; kodlamaya ayrılan süre tek sprinte sıkıştı |
| **Uyarlama** | Son sprint günlük hedeflerle yürütülecek; P0 story'ler bitmeden P1'e geçilmeyecek; her gün kısa daily scrum notu tutulacak |
