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

    def dedektif_vakalari(self, vaka_id):
        sorgu = "SELECT id, baslik, durum, olay_baslangic FROM vakalar WHERE dedektif_id = ? ORDER BY olay_baslangic"
        imlec = self.baglanti.execute(sorgu, (int(vaka_id),))
        return imlec.fetchall()

    def kapat(self):
        self.baglanti.close()