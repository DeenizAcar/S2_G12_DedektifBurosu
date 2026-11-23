# CLAUDE.md — DedektifBurosu (MBP 207 Dönem Sonu Projesi, S2 · G12)

Bu dosya, bu depoda çalışan Claude (ve diğer YZ araçları) için kuralları ve proje bağlamını içerir.
Grubun 3 üyesi de bu dosyayı kullanır. **Önce "Yapay zekâ kuralları" bölümünü oku; bu bölüm her şeyden önce gelir.**

## Proje

Dedektif büroları için vaka, şüpheli ve delil yönetimi yapan; alibi çelişkilerini tespit edip
şüphelileri delillere göre puanlayan Python masaüstü uygulaması.

- Dil: Python 3, GUI: **CustomTkinter** (çizimler için Tkinter `Canvas`), Veri tabanı: **SQLite**
- PyCharm'da açılıp `kod/main.py` ile çalışmalı. Harici kütüphaneler `kod/requirements.txt` içinde.
- Son teslim: **21 Aralık 2026 Pazar 12.00**, tek zip: `S2_G12_DedektifBurosu.zip`
- Depo: https://github.com/DeenizAcar/S2_G12_DedektifBurosu (public)

## Yapay zekâ kuralları (hocanın yönergesi — kesin)

Yönerge, back end'de YZ kullanımını yasaklar. Tespit edilirse OOP puanı (25) sıfırlanır ve
akademik dürüstlük süreci başlar. Bu yüzden:

| Alan | Dosyalar | Claude ne yapabilir |
|---|---|---|
| **Back end: OOP iş mantığı** | `kod/modeller/**`, `kod/veritabani.py` | **Kod YAZMA.** Kod üretme, tamamlama, düzeltme, refactor, **hata ayıklama yok.** Bu dosyaları düzenleme. |
| GUI | `kod/gui/**`, `kod/main.py` | Serbest. Tamamen yazılabilir. |
| SQL / şema | `veritabani.sql`, SQL sorgu metinleri | Yardım serbest. Kullanılan kısım beyan edilir. |
| Dokümantasyon | `README.md`, diyagramlar, sunum | Serbest. İçerik kodla uyumlu olmalı. |

Back end konusunda kullanıcı yardım isterse:
- Python/OOP **kavramlarını** (kalıtım, `@property`, override, try/except, sqlite3 parametreli sorgu…)
  projeden **bağımsız, genel örneklerle** anlatabilirsin.
- Projedeki sınıfın kodunu yazma, eksik metodu tamamlama, hatalı satırı gösterme, "şu satırı şöyle değiştir" deme.
- Kullanıcı ısrar ederse yönergeyi hatırlat ve kibarca reddet.

`VeriTabani` de bir Python sınıfıdır ve OOP puanına sayılır: sınıfın kendisini öğrenci yazar.
İçinde kullanılacak **SQL sorgu metinlerini** (CREATE, SELECT, JOIN…) önerebilirsin.

**Beyan:** README'deki "Yapay Zekâ Kullanım Beyanı" bölümü zorunludur. GUI, SQL veya doküman
ürettiğinde bu bölüme hangi dosya / iş için kullanıldığını bir satırla ekle.

## Mimari

Katmanlar ayrı dosyalarda tutulur. **GUI içinde iş mantığı ve SQL olmaz.** GUI yalnızca model
sınıflarının ve `VeriTabani` sınıfının metotlarını çağırır.

```
kod/
  main.py                 # uygulamayı başlatır
  requirements.txt
  veritabani.py           # VeriTabani sınıfı: tüm SQL burada  (BACK END — YZ yasak)
  modeller/               # iş mantığı sınıfları             (BACK END — YZ yasak)
    kisi.py               # Kisi, Supheli, Tanik, Dedektif
    delil.py              # Delil, FizikselDelil, DijitalDelil, TanikIfadesi
    vaka.py               # Vaka
    sorusturma.py         # Sorusturma (analiz motoru)
  gui/                    # arayüz (YZ serbest)
    ana_pencere.py        # ana panel: vaka listesi, özet
    vaka_detay.py         # sekmeler: kişiler / deliller / alibiler (CRUD)
    zaman_cizelgesi.py    # olaylar + alibiler saat ekseninde, çelişki kırmızı
    iliski_panosu.py      # şüpheli–delil ağı ("kırmızı ipli pano")
    analiz_ekrani.py      # şüphe puanı sıralaması, çelişki raporu
veritabani.sql            # CREATE TABLE + örnek veri (demo vaka) + temel sorgular
README.md
```

GUI bir model metoduna ihtiyaç duyar ve o metot henüz yoksa: metodu **sen yazma**. Kullanıcıya
hangi isimde, hangi parametreyle, ne döndüren bir metoda ihtiyaç olduğunu söyle; sınıf sahibi yazsın.

### Sınıflar (GUI hariç)

- `Kisi` → `Supheli`, `Tanik`, `Dedektif`
- `Delil` → `FizikselDelil`, `DijitalDelil`, `TanikIfadesi` — her alt sınıf `guvenilirlik()`'i farklı hesaplar
  (fiziksel yüksek/sabit, tanık ifadesi zamanla düşer)
- `Vaka` — durum akışı: Açık → Soruşturmada → Çözüldü / Kapandı
- `Sorusturma` — alibi çelişkisi tespiti + şüphe puanı
- `VeriTabani` — tüm SQL işlemleri, parametreli sorgular (`?`), string birleştirme yok

### Tablolar (SQLite)

`dedektifler`, `vakalar` (dedektif_id FK), `kisiler` (tur: supheli/tanik), `vaka_kisileri`
(vaka–kişi çoka-çok, rol), `deliller` (vaka_id FK, kisi_id FK, tur, zaman, yer), `alibiler`
(kisi_id FK, vaka_id FK, baslangic, bitis, yer), `ifadeler`. PK / FK / NOT NULL kısıtları eksiksiz;
`PRAGMA foreign_keys = ON`.

### Ekranlar

Ana panel, Vaka detayı (CRUD), Zaman çizelgesi, İlişki panosu, Analiz ekranı.
Dört CRUD işlemi (ekle, listele, güncelle, sil) arayüzden yapılabilmeli; girişlerde doğrulama,
try/except ve anlamlı `messagebox` hata mesajları olmalı.

## Görev dağılımı

| Üye | İş mantığı sınıfları | GUI ekranı |
|---|---|---|
| 1 | `Kisi`, `Supheli`, `Tanik`, `Dedektif`, `VeriTabani` | Ana panel |
| 2 | `Delil`, `FizikselDelil`, `DijitalDelil`, `TanikIfadesi` | Vaka detayı, İlişki panosu |
| 3 | `Vaka`, `Sorusturma` | Zaman çizelgesi, Analiz ekranı |

(Üye adları ve GitHub kullanıcı adları README'deki tabloda.)

## Git ve kod kuralları

- Bireysel puan commit geçmişine göre verilir: **her üye yalnızca kendi bilgisayarından, kendi hesabıyla
  ve kendi dosyalarını** commit eder. Başka bir üyenin dosyasını onun yerine yazıp commit etme.
- Commit mesajları Türkçe ve açıklayıcı ("Delil sinifi ve guvenilirlik metodu eklendi").
  "guncelleme", "son hali" gibi mesajlar puan düşürür. Commit'ler haftalara yayılmalı.
- Önce Pull, sonra çalış, sonra Commit and Push.
- `.db`, `venv/`, `.idea/` depoya girmez (`.gitignore`). `.db` yalnızca teslim zip'ine konur.
- İsimlendirme: Türkçe, Türkçe karakter yok; sınıflar `PascalCase`, metot/değişkenler `snake_case`.
- Derste görülmeyen ileri düzey yapılardan kaçın (metaclass, decorator fabrikaları, async vb.).
  Sunumda her satır savunulabilmeli.
