# DedektifBurosu

MBP 207 Görsel Programlama — Dönem Sonu Projesi (S2 · G12)

Dedektif büroları için vaka, şüpheli ve delil yönetimi yapan; alibi çelişkilerini tespit edip şüphelileri delillere göre puanlayan masaüstü uygulaması.

## Grup Üyeleri ve Görev Dağılımı

| Üye | GitHub | Sorumlu olduğu sınıflar | GUI ekranı |
|---|---|---|---|
| Deniz Acar | [DeenizAcar](https://github.com/DeenizAcar) | `Kisi`, `Supheli`, `Tanik`, `Dedektif`, `VeriTabani` | Ana panel, kişi yönetimi |
| _Ad Soyad_ | [AhmetRasimVural](https://github.com/AhmetRasimVural) | `Delil`, `FizikselDelil`, `DijitalDelil`, `TanikIfadesi` | Vaka detayı (deliller), ilişki panosu |
| _Ad Soyad_ | [Xavnetex](https://github.com/Xavnetex) | `Vaka`, `Sorusturma` | Zaman çizelgesi, analiz ekranı |

## Kullanılan Teknolojiler

- **GUI modülü:** CustomTkinter
- **Veri tabanı:** SQLite

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

_(Proje ilerledikçe güncellenecek. Back end sınıfları yapay zekâ kullanılmadan yazılmaktadır.)_
