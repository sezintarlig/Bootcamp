# Sprint 2 Raporu (6 – 19 Temmuz 2026)

> Bu sprintin görsel kanıtları (ürün ekran görüntüleri + sprint board): [belgeler/](./belgeler/)

## Sprint Hedefi
Ürün kapsamının tanımlanması ve proje belgelerinin (README, backlog) oluşturulması.

## Ne Yaşandı
- Sprint 1'de yazılan ilk ürün tanımı ("Media Mirror" — film karakter verilerinden **nicel** cinsiyet dağılımı + karakter ajansı çıkaran ve paylaşılabilir "farkındalık kartı" üreten araç) üzerinde çalışıldı.
- Sprint sonunda bu kapsamın iki zayıflığı görüldü:
  1. **Teknik belirsizlik:** "Karakter ajansı"nın TMDb verisinden nicel olarak çıkarılıp çıkarılamayacağı netleştirilemedi.
  2. **Vizyon uyumsuzluğu:** Asıl anlatılmak istenen şeyin sayısal bir dağılım değil, kadın karakterlerin konumuna dair **nitel, feminist bir yorum** olduğu netleşti.
- 19 Temmuz'da yapılandırılmış bir kapsam sorgulama oturumu yapıldı; ürün baştan tanımlandı.
- Netleşen kapsamın ardından aynı gün MVP çekirdeği kodlandı ve gerçek API'lerle test edildi: TMDb servisi, 4 agent'lı pipeline, hafıza katmanı, Streamlit arayüzü, özet kart ve 9 birim testi.

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
- ✅ MVP çekirdeği kodlandı ve gerçek API'lerle uçtan uca test edildi (backlog #1–#11, #13)
- ✅ Son sprint gün bazında planlandı
- ⏭️ Son Sprint'e devreden: deployment (#12), gerçek kullanım testi/cila, video ve teslim seti

## Retrospektif
| | |
|---|---|
| **İyi giden** | Kapsam sorunları teslime 2 hafta kala fark edilip köklü biçimde çözüldü; belirsiz kısımlar (ajans ölçümü) ürüne girmeden ayıklandı; net kapsam sayesinde MVP tek günde kodlanabildi |
| **Zorlayan** | Fikrin netleşmesi beklenenden uzun sürdü; sprintin büyük bölümü kod üretmeden geçti |
| **Uyarlama** | Son sprint günlük hedeflerle yürütülecek; her gün kısa daily scrum notu tutulacak; kalan işler (deploy, video) erken bitirilip tampon bırakılacak |
