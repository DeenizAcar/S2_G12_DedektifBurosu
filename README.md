# DedektifBurosu

MBP 207 Görsel Programlama — Dönem Sonu Projesi (S2 · G12)

Dedektif büroları için vaka, şüpheli ve delil yönetimi yapan; alibi çelişkilerini tespit edip şüphelileri delillere göre puanlayan masaüstü uygulaması.

## Grup Üyeleri ve Görev Dağılımı

| Üye | GitHub | Sorumlu olduğu sınıflar | GUI ekranı |
|---|---|---|---|
| Deniz Acar | [DeenizAcar](https://github.com/DeenizAcar) | `Kisi`, `Supheli`, `Tanik`, `Dedektif`, `VeriTabani` | Giriş ekranı, vaka masası, şahıs arşivi |
| _Ad Soyad_ | [AhmetRasimVural](https://github.com/AhmetRasimVural) | `Delil`, `FizikselDelil`, `DijitalDelil`, `TanikIfadesi` | Vaka dosyası (deliller), ilişki panosu |
| _Ad Soyad_ | [Xavnetex](https://github.com/Xavnetex) | `Vaka`, `Sorusturma` | Yeni vaka, zaman çizelgesi, şüphe analizi |

## Kullanılan Teknolojiler

- **GUI modülü:** CustomTkinter (çizimler için Tkinter `Canvas`)
- **Görüntü işleme:** Pillow (kâğıt, masa ve damga dokuları kodla üretilir)
- **Veri tabanı:** SQLite

## Arayüz

Uygulama, Soğuk Savaş dönemi bir devlet dairesindeki dedektif masası olarak tasarlandı.
Dedektif sicil numarasıyla giriş yapar, ardından masadaki nesnelere tıklayarak ekranlara geçer:

| Masadaki nesne | Açılan ekran |
|---|---|
| Vaka dosyaları (Gelen Evrak) | Vaka dosyası |
| Şahıs arşivi | Kişiler (şüpheli ve tanıklar) |
| Daktilo | Yeni vaka kaydı |
| Mantar pano | İlişki panosu |
| Teleks şeridi | Zaman çizelgesi |
| Not defteri | Şüphe analizi |
| Radyo | Sesi aç / kapat |

Efektler: damga basma animasyonu, daktilo yazısı, hatalı girişte titreme ve ses efektleri.

## Kurulum ve Çalıştırma

1. Projeyi PyCharm'da açın.
2. `requirements.txt` için PyCharm'ın önerdiği **Install requirements** uyarısını kabul edin.
3. `kod/main.py` dosyasını çalıştırın.

## GitHub Deposu

https://github.com/DeenizAcar/S2_G12_DedektifBurosu

## Yapay Zekâ Kullanım Beyanı

| Araç | Kullanıldığı dosya / iş |
|---|---|
| Claude | `veritabani.sql`: tablo tasarımı, örnek veri (demo vaka senaryosu) ve temel sorgular |
| Claude | `README.md` şablonu |
| Claude | `kod/main.py` ve `kod/gui/` klasörü: pencere akışı, giriş ekranı, vaka masası, geçici sayfalar, tema, dokular ve efektler |
| Claude | `kod/gui/sesler/*.wav`: ses efektleri Python koduyla sentezlendi (hazır ses dosyası kullanılmadı) |

| Claude | Back end (`kod/modeller/`, `kod/veritabani.py`): kod yazdırılmadı. Kavram açıklaması, hata mesajlarının anlamı ve hataların yeri/nedeni hakkında açıklama alındı; düzeltmeler öğrenciler tarafından yazıldı. |

_(Proje ilerledikçe güncellenecek.)_
