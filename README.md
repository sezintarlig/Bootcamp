# Media Mirror (Medya Aynası)

## Takım İsmi
Media Mirror — Solo Takım *(5 kişilik olması gereken takım, iletişim kopukluğu nedeniyle tek kişi tarafından yürütülmektedir)*

## Takım Rolleri
Bu proje tek kişi tarafından yürütülmektedir; aşağıdaki roller aynı kişi (Sezin) tarafından üstlenilmiştir:
- **Product Owner:** Ürün vizyonu, kapsam kararları, backlog önceliklendirme
- **Scrum Master:** Sprint planlama, süreç takibi, engellerin yönetimi
- **Developer:** Teknik geliştirme, API entegrasyonu, AI agent orkestrasyonu

## Ürün İsmi
Media Mirror (Medya Aynası)

## Ürün Açıklaması
İzleyicilerin bir film hakkındaki temsil (representation) örüntülerini kolayca görebilmesini sağlayan bir yapay zeka aracı. Kullanıcı bir film adı girer; sistem o filmin karakter ve rol verilerini analiz ederek, cinsiyet dağılımı ve karakter ajansı (karar alma gücü) açısından çarpıcı, paylaşılabilir bir "farkındalık kartı" üretir.

Var olan araçlar (örn. Bechdel testi) tek boyutlu ve basit "geçti/kaldı" mantığıyla çalışırken, Media Mirror niceliksel bir dağılım sunarak daha zengin bir görünüm sağlar.

## Ürün Özellikleri
- Film adı girişi ile analiz başlatma
- TMDb API üzerinden karakter/oyuncu verisi çekme
- Yapay zeka destekli çok adımlı analiz (3 agent orkestrasyonu):
  1. **Veri Çıkarıcı Agent:** Film verisini TMDb'den çeker, karakter listesini hazırlar
  2. **Temsil Analiz Agent:** Cinsiyet dağılımı ve karakter ajansını değerlendirir
  3. **Kart Üretici Agent:** Sonucu çarpıcı, paylaşılabilir bir kart formatında sunar
- Basit, kullanıcı dostu web arayüzü (Streamlit)

### Gelecek Geliştirmeler (Kapsam Dışı — Roadmap)
- Akademik/detaylı analiz modu (teorik çerçeve referanslarıyla)
- Ek analiz boyutları: yaş temsili, meslek/statü klişeleri, ırk/etnisite, engellilik temsili
- Streamlit Community Cloud üzerinde canlı yayın

## Hedef Kitle
1. **Genel izleyici kitlesi:** Film/dizi izleyenler, ebeveynler, öğretmenler, medya okuryazarlığı eğitimcileri
2. **Akademik/uzman kitle (ileride):** Medya çalışmaları, iletişim, kadın çalışmaları alanında araştırmacılar

## Product Backlog
Bkz. [BACKLOG.md](./BACKLOG.md)

## Değerlendirme Kriterleri (YZ Kategorisi)
| Kriter | Puan |
|---|---|
| İhtiyaç ve Çözüm Eşleşmesi | 20 |
| Kullanıcı Değeri ve Deneyimi | 10 |
| Pazar Potansiyeli | 10 |
| Fonksiyonel Yeterlilik | 15 |
| Ürün Bütünlüğü | 10 |
| Yapay Zeka Öğeleri | 35 |
