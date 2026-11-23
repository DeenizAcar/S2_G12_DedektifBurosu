import sqlite3
from pathlib import Path


class VeriTabani:
    def __init__(self, dosya_yolu):
        dosya_yolu = Path(dosya_yolu)
        daha_once_var_mi = dosya_yolu.exists()

        self.baglanti = sqlite3.connect(dosya_yolu)
        self.baglanti.execute("PRAGMA foreign_keys = ON")

        if not daha_once_var_mi:
            sql_yolu = Path(__file__).resolve().parent.parent / "veritabani.sql"
            sql_betigi = sql_yolu.read_text(encoding="utf-8")
            self.baglanti.executescript(sql_betigi)
            self.baglanti.commit()

    def dedektif_bul(self, sicil_no):
        sorgu = "SELECT id, ad, soyad, sicil_no FROM dedektifler WHERE sicil_no = ?"
        imlec = self.baglanti.execute(sorgu, (sicil_no,))
        return imlec.fetchone()

    def dedektif_vakalari(self, dedektif_id):
        sorgu = "SELECT id, baslik, durum, olay_baslangic FROM vakalar WHERE dedektif_id = ? ORDER BY olay_baslangic"
        imlec = self.baglanti.execute(sorgu, (int(dedektif_id),))
        return imlec.fetchall()

    def kapat(self):
        self.baglanti.close()

    def kisileri_listele(self):
        sorgu = "SELECT id, ad, soyad, tc_no, dogum_tarihi, telefon, adres FROM kisiler ORDER BY soyad, ad"
        imlec = self.baglanti.execute(sorgu)
        return imlec.fetchall()

    def kisi_ekle(self, kisi):
        sorgu = "INSERT INTO kisiler (ad, soyad, tc_no, dogum_tarihi, telefon, adres) VALUES (?, ?, ?, ?, ?, ?)"
        degerler = (kisi.ad, kisi.soyad, kisi.tc, kisi.d_tarihi, kisi.telefon, kisi.adres)
        imlec = self.baglanti.execute(sorgu, degerler)
        self.baglanti.commit()
        kisi.id = imlec.lastrowid
        return kisi.id

    def kisi_guncelle(self, kisi):
        sorgu = "UPDATE kisiler SET ad = ?, soyad = ?, tc_no = ?, dogum_tarihi = ?, telefon = ?, adres = ? WHERE id = ?"
        degerler = (kisi.ad, kisi.soyad, kisi.tc, kisi.d_tarihi, kisi.telefon, kisi.adres, kisi.id)
        self.baglanti.execute(sorgu, degerler)
        self.baglanti.commit()

    def kisi_sil(self, kisi_id):
        sorgu = "DELETE FROM kisiler WHERE id = ?"
        degerler = (kisi_id,)
        self.baglanti.execute(sorgu, degerler)
        self.baglanti.commit()