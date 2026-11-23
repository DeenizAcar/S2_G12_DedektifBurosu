-- =====================================================================
--  DedektifBurosu — Veri Tabanı (SQLite)
--  MBP 207 · S2 · G12
--
--  İçerik:
--    1. Tablo oluşturma (CREATE TABLE)
--    2. Örnek veri (INSERT) — "Moda Sahafı Cinayeti" demo vakası
--    3. Uygulamanın kullandığı temel sorgular
--
--  Tarih/saat biçimi her yerde 'YYYY-MM-DD HH:MM' (metin).
--  Bu biçimde metin karşılaştırması (<, >, BETWEEN) zaman sırasıyla aynı
--  sonucu verir; ayrı bir tarih tipine gerek kalmaz.
-- =====================================================================

PRAGMA foreign_keys = ON;   -- SQLite'ta FK kısıtları varsayılan olarak kapalıdır

DROP TABLE IF EXISTS alibiler;
DROP TABLE IF EXISTS deliller;
DROP TABLE IF EXISTS vaka_kisileri;
DROP TABLE IF EXISTS vakalar;
DROP TABLE IF EXISTS kisiler;
DROP TABLE IF EXISTS dedektifler;

-- ---------------------------------------------------------------------
-- 1. TABLOLAR
-- ---------------------------------------------------------------------

-- Büroda çalışan dedektifler
CREATE TABLE dedektifler (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    ad          TEXT    NOT NULL,
    soyad       TEXT    NOT NULL,
    sicil_no    TEXT    NOT NULL UNIQUE,
    telefon     TEXT
);

-- Vakalarla ilgili tüm kişiler (şüpheli, tanık, kurban).
-- Kişinin rolü burada değil vaka_kisileri tablosunda tutulur:
-- aynı kişi bir vakada tanık, başka bir vakada şüpheli olabilir.
CREATE TABLE kisiler (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    ad            TEXT    NOT NULL,
    soyad         TEXT    NOT NULL,
    tc_no         TEXT    UNIQUE CHECK (tc_no IS NULL OR length(tc_no) = 11),
    dogum_tarihi  TEXT,
    telefon       TEXT,
    adres         TEXT
);

-- Vakalar. fail_id vaka çözülene kadar NULL kalır.
CREATE TABLE vakalar (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    baslik       TEXT    NOT NULL,
    aciklama     TEXT,
    olay_yeri    TEXT    NOT NULL,
    olay_baslangic TEXT  NOT NULL,   -- olayın tahmini zaman aralığı
    olay_bitis   TEXT    NOT NULL,
    durum        TEXT    NOT NULL DEFAULT 'Açık'
                 CHECK (durum IN ('Açık', 'Soruşturmada', 'Çözüldü', 'Kapandı')),
    dedektif_id  INTEGER NOT NULL REFERENCES dedektifler(id),
    fail_id      INTEGER REFERENCES kisiler(id),
    CHECK (olay_bitis >= olay_baslangic)
);

-- Vaka <-> kişi çoka-çok ilişkisi; kişinin o vakadaki rolü
CREATE TABLE vaka_kisileri (
    vaka_id   INTEGER NOT NULL REFERENCES vakalar(id) ON DELETE CASCADE,
    kisi_id   INTEGER NOT NULL REFERENCES kisiler(id) ON DELETE CASCADE,
    rol       TEXT    NOT NULL CHECK (rol IN ('Şüpheli', 'Tanık', 'Kurban')),
    motif     TEXT,                  -- yalnızca şüpheliler için anlamlı
    PRIMARY KEY (vaka_id, kisi_id)
);

-- Deliller. Üç delil türü tek tabloda tutulur (tur sütunu);
-- türe özgü sütunlar diğer türlerde NULL kalır.
--   zaman : delilin kişiyi o yerde gösterdiği an (bilinmiyorsa NULL,
--           örn. parmak izinin ne zaman bırakıldığı bilinmez)
--   kayit_tarihi : delilin büroya kaydedildiği an (tanık ifadesinin
--           olaydan ne kadar sonra alındığını hesaplamak için)
CREATE TABLE deliller (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    vaka_id       INTEGER NOT NULL REFERENCES vakalar(id) ON DELETE CASCADE,
    kisi_id       INTEGER REFERENCES kisiler(id) ON DELETE SET NULL,  -- delilin işaret ettiği kişi
    tur           TEXT    NOT NULL CHECK (tur IN ('Fiziksel', 'Dijital', 'Tanık İfadesi')),
    aciklama      TEXT    NOT NULL,
    yer           TEXT    NOT NULL,
    zaman         TEXT,
    kayit_tarihi  TEXT    NOT NULL,
    -- Fiziksel delil
    analiz_turu   TEXT,              -- Parmak izi, DNA, Ayak izi...
    -- Dijital delil
    kaynak        TEXT,              -- Baz istasyonu, Kamera, Fiş...
    -- Tanık ifadesi
    tanik_id      INTEGER REFERENCES kisiler(id) ON DELETE SET NULL
);

-- Şüphelilerin beyan ettiği alibiler
CREATE TABLE alibiler (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    vaka_id      INTEGER NOT NULL REFERENCES vakalar(id) ON DELETE CASCADE,
    kisi_id      INTEGER NOT NULL REFERENCES kisiler(id) ON DELETE CASCADE,
    yer          TEXT    NOT NULL,
    baslangic    TEXT    NOT NULL,
    bitis        TEXT    NOT NULL,
    aciklama     TEXT,
    CHECK (bitis > baslangic)
);

-- ---------------------------------------------------------------------
-- 2. ÖRNEK VERİ
-- ---------------------------------------------------------------------

INSERT INTO dedektifler (ad, soyad, sicil_no, telefon) VALUES
    ('Nur',    'Kaya',   'D-1042', '0532 410 10 42'),
    ('Orhan',  'Tekin',  'D-0877', '0533 287 08 77');

INSERT INTO kisiler (ad, soyad, tc_no, dogum_tarihi, telefon, adres) VALUES
    ('Kemal',  'Aksoy',  '10000000146', '1958-03-12', NULL,             'Moda, Kadıköy'),         -- 1 kurban
    ('Selin',  'Aksoy',  '20000000282', '1994-07-21', '0541 220 11 33', 'Moda, Kadıköy'),         -- 2 yeğen
    ('Murat',  'Demir',  '30000000318', '1979-11-02', '0532 330 44 55', 'Beşiktaş'),              -- 3 rakip sahaf
    ('Can',    'Yıldız', '40000000454', '2003-01-15', '0555 440 66 77', 'Kadıköy'),               -- 4 çırak
    ('Hakan',  'Erdem',  '50000000590', '1968-09-30', '0536 550 88 99', 'Cihangir, Beyoğlu'),     -- 5 koleksiyoner
    ('Ayten',  'Şahin',  '60000000626', '1971-05-08', '0542 660 12 34', 'Moda, Kadıköy'),         -- 6 karşı komşu (tanık)
    ('Burak',  'Öz',     '70000000762', '1980-02-17', '0544 770 56 78', 'Beşiktaş'),              -- 7 Murat'ın arkadaşı (tanık)
    ('Leyla',  'Arslan', '80000000898', '1985-12-04', '0539 880 90 12', 'Nişantaşı, Şişli'),      -- 8 galeri sahibi
    ('Emre',   'Kılınç', '90000000934', '1990-06-25', '0546 990 23 45', 'Nişantaşı, Şişli');      -- 9 galeri bekçisi

-- Vaka 1: demo vakası (açık). Vaka 2: daha önce çözülmüş küçük bir vaka.
INSERT INTO vakalar (baslik, aciklama, olay_yeri, olay_baslangic, olay_bitis, durum, dedektif_id, fail_id) VALUES
    ('Moda Sahafı Cinayeti',
     'Sahaf sahibi Kemal Aksoy dükkânında ölü bulundu. Kasa açık, nadir kitap rafı dağınık. Otopsiye göre ölüm 21:00-22:00 arasında.',
     'Moda Sahafı', '2026-11-14 21:00', '2026-11-14 22:00', 'Soruşturmada', 1, NULL),
    ('Nişantaşı Kayıp Tablo',
     'Galeriden 19. yüzyıla ait bir yağlıboya tablo kayboldu.',
     'Arslan Galeri', '2026-10-02 01:00', '2026-10-02 05:00', 'Çözüldü', 2, 9);

INSERT INTO vaka_kisileri (vaka_id, kisi_id, rol, motif) VALUES
    (1, 1, 'Kurban',  NULL),
    (1, 2, 'Şüpheli', 'Kurbanın tek mirasçısı; dükkân ve kitap koleksiyonu ona kalıyor.'),
    (1, 3, 'Şüpheli', 'Kurbana yüklü miktarda borcu var, iki hafta önce tartıştıkları biliniyor.'),
    (1, 4, 'Şüpheli', 'Kurbanın çırağı. Dükkândan nadir kitap çalıp internetten sattığı ortaya çıkmak üzereydi.'),
    (1, 5, 'Şüpheli', 'Satılmayan bir ilk baskı kitap yüzünden kurbanla aynı gün tartıştı.'),
    (1, 6, 'Tanık',   NULL),
    (1, 7, 'Tanık',   NULL),
    (2, 8, 'Tanık',   NULL),
    (2, 9, 'Şüpheli', 'Gece vardiyasında tek başınaydı, kumar borcu var.');

-- Vaka 1 delilleri
INSERT INTO deliller (vaka_id, kisi_id, tur, aciklama, yer, zaman, kayit_tarihi, analiz_turu, kaynak, tanik_id) VALUES
    -- Can Yıldız (gerçek fail): alibisi sinema ama telefonu ve tanık onu dükkânda gösteriyor
    (1, 4, 'Dijital',       'Can Yıldız''ın telefonu olay saatinde dükkânı kapsayan baz istasyonuna bağlanmış.',
        'Moda Sahafı',      '2026-11-14 21:20', '2026-11-16 10:00', NULL,          'Baz istasyonu kaydı', NULL),
    (1, 4, 'Tanık İfadesi', 'Karşı komşu, 21:40 civarı dükkândan aceleyle çıkan genç bir adam gördü; fotoğraftan Can Yıldız''ı tanıdı.',
        'Moda Sahafı',      '2026-11-14 21:40', '2026-11-20 14:30', NULL,          NULL,                  6),
    (1, 4, 'Fiziksel',      'Açık bırakılan kasa çekmecesinde Can Yıldız''ın parmak izi.',
        'Moda Sahafı',      NULL,               '2026-11-15 09:00', 'Parmak izi',  NULL,                  NULL),
    (1, 4, 'Dijital',       'Sinema bileti satın alma kaydı (19:30 seansı).',
        'Kadıköy Sineması', '2026-11-14 19:15', '2026-11-16 11:00', NULL,          'Bilet satış sistemi', NULL),
    -- Selin Aksoy: güçlü motif, ama alibisi dijital kayıtla doğrulanıyor
    (1, 2, 'Dijital',       'Akıllı TV izleme kaydı: 20:30-23:10 arası evde kesintisiz yayın.',
        'Selin Aksoy Evi',  '2026-11-14 21:15', '2026-11-17 16:00', NULL,          'Akıllı TV kaydı',     NULL),
    -- Murat Demir: borç motifi, alibisi hem fiş hem tanıkla doğrulanıyor
    (1, 3, 'Dijital',       'Restoran hesap fişi, kredi kartıyla ödenmiş.',
        'Beşiktaş Balıkçı', '2026-11-14 22:10', '2026-11-16 12:00', NULL,          'Ödeme kaydı',         NULL),
    (1, 3, 'Tanık İfadesi', 'Burak Öz, Murat Demir ile 20:00-22:30 arası birlikte yemek yediklerini söylüyor.',
        'Beşiktaş Balıkçı', '2026-11-14 21:00', '2026-11-15 15:00', NULL,          NULL,                  7),
    -- Hakan Erdem: dükkânda izi var ama olay saatinden önce; doğrulanamayan alibi
    (1, 5, 'Fiziksel',      'Nadir kitap rafındaki bir kitabın kapağında Hakan Erdem''in parmak izi.',
        'Moda Sahafı',      NULL,               '2026-11-15 09:30', 'Parmak izi',  NULL,                  NULL),
    (1, 5, 'Tanık İfadesi', 'Karşı komşu, saat 18:00 civarı Hakan Erdem''in kurbanla dükkânda yüksek sesle tartıştığını duydu.',
        'Moda Sahafı',      '2026-11-14 18:00', '2026-11-15 11:00', NULL,          NULL,                  6),
    -- Henüz kimseyle eşleşmemiş delil
    (1, NULL, 'Fiziksel',   'Arka kapı önünde 42 numara spor ayakkabı izi.',
        'Moda Sahafı',      NULL,               '2026-11-15 10:00', 'Ayak izi',    NULL,                  NULL);

-- Vaka 2 delili
INSERT INTO deliller (vaka_id, kisi_id, tur, aciklama, yer, zaman, kayit_tarihi, analiz_turu, kaynak, tanik_id) VALUES
    (2, 9, 'Dijital', 'Galeri kamerası 03:12''de bekçinin tabloyu arka kapıdan çıkardığını gösteriyor.',
        'Arslan Galeri', '2026-10-02 03:12', '2026-10-03 09:00', NULL, 'Güvenlik kamerası', NULL);

-- Alibiler
INSERT INTO alibiler (vaka_id, kisi_id, yer, baslangic, bitis, aciklama) VALUES
    (1, 2, 'Selin Aksoy Evi',  '2026-11-14 20:30', '2026-11-14 23:00', 'Evde tek başına dizi izlediğini söylüyor.'),
    (1, 3, 'Beşiktaş Balıkçı', '2026-11-14 20:00', '2026-11-14 22:30', 'Arkadaşı Burak Öz ile yemekte olduğunu söylüyor.'),
    (1, 4, 'Kadıköy Sineması', '2026-11-14 19:30', '2026-11-14 22:00', 'Film bitene kadar sinemada olduğunu söylüyor.'),
    (1, 5, 'Hakan Erdem Evi',  '2026-11-14 19:00', '2026-11-14 23:30', 'Tartışmadan sonra eve gidip uyuduğunu söylüyor.'),
    (2, 9, 'Arslan Galeri',    '2026-10-02 00:00', '2026-10-02 06:00', 'Bütün gece görev başında olduğunu söylüyor.');

-- ---------------------------------------------------------------------
-- 3. UYGULAMANIN KULLANDIĞI TEMEL SORGULAR
--    Uygulamada değerler '?' yer tutucularıyla (parametreli) verilir;
--    string birleştirme ile sorgu kurulmaz.
-- ---------------------------------------------------------------------

-- Ana panel: vakalar ve sorumlu dedektif
-- SELECT v.id, v.baslik, v.durum, v.olay_baslangic, d.ad || ' ' || d.soyad AS dedektif
-- FROM vakalar v
-- JOIN dedektifler d ON d.id = v.dedektif_id
-- ORDER BY v.olay_baslangic DESC;

-- Ana panel: duruma göre vaka sayıları
-- SELECT durum, COUNT(*) FROM vakalar GROUP BY durum;

-- Vaka detayı: bir vakadaki kişiler ve rolleri
-- SELECT k.id, k.ad, k.soyad, vk.rol, vk.motif
-- FROM vaka_kisileri vk
-- JOIN kisiler k ON k.id = vk.kisi_id
-- WHERE vk.vaka_id = ?
-- ORDER BY vk.rol;

-- Vaka detayı: bir vakanın delilleri (bağlı kişi adıyla)
-- SELECT dl.*, k.ad || ' ' || k.soyad AS kisi
-- FROM deliller dl
-- LEFT JOIN kisiler k ON k.id = dl.kisi_id
-- WHERE dl.vaka_id = ?
-- ORDER BY dl.zaman;

-- Analiz: bir kişinin o vakadaki alibileri ve zamanı bilinen delilleri
-- SELECT * FROM alibiler WHERE vaka_id = ? AND kisi_id = ?;
-- SELECT * FROM deliller WHERE vaka_id = ? AND kisi_id = ? AND zaman IS NOT NULL;

-- CRUD örnekleri (kisiler tablosu; diğer tablolar aynı kalıpla)
-- INSERT INTO kisiler (ad, soyad, tc_no, dogum_tarihi, telefon, adres) VALUES (?, ?, ?, ?, ?, ?);
-- UPDATE kisiler SET ad = ?, soyad = ?, telefon = ?, adres = ? WHERE id = ?;
-- DELETE FROM kisiler WHERE id = ?;

-- Vakayı çözme
-- UPDATE vakalar SET durum = 'Çözüldü', fail_id = ? WHERE id = ?;
