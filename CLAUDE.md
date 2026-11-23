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
| **Back end: OOP iş mantığı** | `kod/modeller/**`, `kod/veritabani.py` | **Kod YAZMA.** Kod üretme, tamamlama, refactor yok; bu dosyaları düzenleme. Yalnızca "öğretmen modu" (aşağıda). |
| GUI | `kod/gui/**`, `kod/main.py` | Serbest. Tamamen yazılabilir. |
| SQL / şema | `veritabani.sql`, SQL sorgu metinleri | Yardım serbest. Kullanılan kısım beyan edilir. |
| Dokümantasyon | `README.md`, diyagramlar, sunum | Serbest. İçerik kodla uyumlu olmalı. |

Back end konusunda kullanıcı yardım isterse **öğretmen modu** geçerlidir (grupla anlaşıldı):
- Python/OOP **kavramlarını** (kalıtım, `@property`, override, try/except, sqlite3 parametreli sorgu…)
  genel örneklerle anlatabilirsin.
- Öğrencinin yazdığı kodu okuyup **hatanın yerini (dosya/satır) ve nedenini** söyleyebilirsin
  ("19. satırda setter'ın adı property'yle aynı olmalı, çünkü..."). Tarifi Türkçe maddelerle verebilirsin.
- **Düzeltilmiş kodu, eksik metodu veya sınıfın kendisini yazma**; çözümü kod bloğu olarak verme.
  Düzeltmeyi öğrenci kendi eliyle yapar. Proje sınıfıyla aynı yapıda "örnek" yazarak dolaylı kod verme.
- Back end dosyalarını düzenleme; kontrol listesi gibi geçici dosyalar `kod/deneme_*.py` adıyla
  yazılabilir (depoya girmez).
- README beyanında öğretmen modu kullanıldığı yazılı olmalı.

`VeriTabani` de bir Python sınıfıdır ve OOP puanına sayılır: sınıfın kendisini öğrenci yazar.
İçinde kullanılacak **SQL sorgu metinlerini** (CREATE, SELECT, JOIN…) önerebilirsin.

**Beyan:** README'deki "Yapay Zekâ Kullanım Beyanı" bölümü zorunludur. GUI, SQL veya doküman
ürettiğinde bu bölüme hangi dosya / iş için kullanıldığını bir satırla ekle.

## Mimari

Katmanlar ayrı dosyalarda tutulur. **GUI içinde iş mantığı ve SQL olmaz.** GUI yalnızca model
sınıflarının ve `VeriTabani` sınıfının metotlarını çağırır.

```
kod/
  main.py                 # uygulamayı başlatır, VeriTabani nesnesini pencereye verir
  requirements.txt        # customtkinter, pillow
  veritabani.py           # VeriTabani sınıfı: tüm SQL burada  (BACK END — YZ yasak)
  modeller/               # iş mantığı sınıfları             (BACK END — YZ yasak)
    kisi.py               # Kisi, Supheli, Tanik, Dedektif
    delil.py              # Delil, FizikselDelil, DijitalDelil, TanikIfadesi
    vaka.py               # Vaka
    sorusturma.py         # Sorusturma (analiz motoru)
  gui/                    # arayüz (YZ serbest)
    ana_pencere.py        # ekran akışı: giriş -> masa -> ekranlar; SAYFALAR sözlüğü
    sahne.py              # Sahne taban sınıfı: masa arka planı, ölçekleme, tıklanabilir nesneler
    giris_ekrani.py       # personel kartıyla dedektif girişi
    masa.py               # ana ekran: masadaki nesneler ekranlara açılır
    yapim_asamasinda.py   # henüz yazılmamış ekranlar için geçici "iç yazışma" sayfası
    tema.py               # renkler, yazı tipleri, kâğıt temalı Treeview stili
    dokular.py            # Pillow ile kâğıt/masa/kraft/damga görüntüleri
    efektler.py           # Ses, damga_bas, daktilo_yaz, titret
    sesler/*.wav          # kodla sentezlenmiş ses efektleri
veritabani.sql            # CREATE TABLE + örnek veri (demo vaka) + temel sorgular
README.md
```

GUI bir model metoduna ihtiyaç duyar ve o metot henüz yoksa: metodu **sen yazma**. Kullanıcıya
hangi isimde, hangi parametreyle, ne döndüren bir metoda ihtiyaç olduğunu söyle; sınıf sahibi yazsın.

### Arayüz ↔ back end sözleşmesi

GUI, `VeriTabani` nesnesinden (`self.uyg.vt`) şu metotları bekler. Yeni bir ekran yeni metot
gerektirirse bu listeye eklenir. `vt` `None` ise ekranlar "bağlantısız" modda çalışmalı.

| Metot | Döndürür | Kullanan ekran |
|---|---|---|
| `dedektif_bul(sicil_no)` | `(id, ad, soyad, sicil_no)` veya `None` | giriş |
| `dedektif_vakalari(dedektif_id)` | `[(vaka_id, baslik, durum, olay_baslangic), ...]` | masa |

### Görsel dil

Soğuk Savaş dönemi devlet dairesi: zeytin yeşili metal masa, krem formlar, kraft dosyalar,
mürekkep damgaları, daktilo yazısı (`Courier New`). Yeni ekranlar `Sahne` sınıfından türetilir,
renkleri `tema.RENKLER`'den alır, efektleri `efektler` modülünden kullanır. Hazır görsel/ses
dosyası eklenmez; dokular `dokular.py` ile üretilir. Belirli bir oyunun görünümü kopyalanmaz.

Yeni ekran bağlamak: `ana_pencere.py` içinde `sayfa_ac()` ilgili anahtar için
`YapimAsamasinda` yerine yeni sınıfı oluşturacak şekilde güncellenir.

### Sınıflar (GUI hariç)

- `Kisi` → `Supheli`, `Tanik`, `Dedektif`
- `Delil` → `FizikselDelil`, `DijitalDelil`, `TanikIfadesi` — her alt sınıf `guvenilirlik()`'i farklı hesaplar
  (fiziksel yüksek/sabit, tanık ifadesi zamanla düşer)
- `Vaka` — durum akışı: Açık → Soruşturmada → Çözüldü / Kapandı
- `Sorusturma` — alibi çelişkisi tespiti + şüphe puanı
- `VeriTabani` — tüm SQL işlemleri, parametreli sorgular (`?`), string birleştirme yok

### Tablolar (SQLite)

Şema `veritabani.sql` içindedir (6 tablo): `dedektifler`, `kisiler`, `vakalar` (dedektif_id FK,
fail_id FK), `vaka_kisileri` (vaka–kişi çoka-çok; `rol`: Şüpheli/Tanık/Kurban, `motif`),
`deliller` (vaka_id FK, kisi_id FK, tanik_id FK; `tur`: Fiziksel/Dijital/Tanık İfadesi; türe
özgü sütunlar diğer türlerde NULL), `alibiler` (vaka_id FK, kisi_id FK, yer, baslangic, bitis).
Kişinin rolü `kisiler`'de değil `vaka_kisileri`'nde tutulur. Tarih biçimi `'YYYY-MM-DD HH:MM'`.
PK / FK / NOT NULL / CHECK kısıtları eksiksiz; `PRAGMA foreign_keys = ON`.

Demo vaka "Moda Sahafı Cinayeti": gerçek fail Can Yıldız (alibisi sinema, ama telefonu ve tanık
onu olay yerinde gösteriyor). Selin (miras) ve Hakan (dükkânda parmak izi, ama olaydan önce)
yanıltıcı ipuçlarıdır. Alibi çelişkisi yalnızca Can'da çıkmalı.

### Ekranlar

Giriş, Masa (ana ekran), Şahıs Arşivi, Vaka Dosyası, Yeni Vaka, İlişki Panosu, Zaman Çizelgesi,
Şüphe Analizi. Dört CRUD işlemi (ekle, listele, güncelle, sil) arayüzden yapılabilmeli; girişlerde
doğrulama, try/except ve anlamlı `messagebox` hata mesajları olmalı. Doğrulama kuralları model
sınıfında (setter `ValueError` fırlatır), GUI yalnızca hatayı yakalayıp gösterir.

## Görev dağılımı

| Üye | İş mantığı sınıfları | GUI ekranı |
|---|---|---|
| Deniz Acar (DeenizAcar) | `Kisi`, `Supheli`, `Tanik`, `Dedektif`, `VeriTabani` | Giriş, Masa, Şahıs Arşivi |
| AhmetRasimVural | `Delil`, `FizikselDelil`, `DijitalDelil`, `TanikIfadesi` | Vaka Dosyası, İlişki Panosu |
| Xavnetex | `Vaka`, `Sorusturma` | Yeni Vaka, Zaman Çizelgesi, Şüphe Analizi |

(Üye adları ve GitHub kullanıcı adları README'deki tabloda.)

## Git ve kod kuralları

- Bireysel puan commit geçmişine göre verilir: **her üye yalnızca kendi bilgisayarından, kendi hesabıyla
  ve kendi dosyalarını** commit eder. Başka bir üyenin dosyasını onun yerine yazıp commit etme.
- Commit mesajları Türkçe ve açıklayıcı ("Delil sinifi ve guvenilirlik metodu eklendi").
  "guncelleme", "son hali" gibi mesajlar puan düşürür. Commit'ler haftalara yayılmalı.
- Commit mesajlarına `Co-Authored-By: Claude` satırı **eklenmez**; YZ kullanımı yalnızca README beyanında yazılır.
- Önce Pull, sonra çalış, sonra Commit and Push.
- Kurulum: PyCharm `uv` ile `.venv` oluşturur; paketler için `uv pip install -r kod/requirements.txt`.
  `pyproject.toml` ve `uv.lock` depoya girmez.
- `.db`, `venv/`, `.idea/` depoya girmez (`.gitignore`). `.db` yalnızca teslim zip'ine konur.
- İsimlendirme: Türkçe, Türkçe karakter yok; sınıflar `PascalCase`, metot/değişkenler `snake_case`.
- Derste görülmeyen ileri düzey yapılardan kaçın (metaclass, decorator fabrikaları, async vb.).
  Sunumda her satır savunulabilmeli.
