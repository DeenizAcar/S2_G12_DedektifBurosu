"""Uygulama penceresi: ekranlar arası geçişi yönetir.

Akış: Giriş ekranı -> Masa -> (masadaki nesneye göre) ilgili ekran -> Masa ...
GUI içinde SQL veya iş mantığı yoktur; veriler VeriTabani nesnesinden (vt) istenir.
"""
import customtkinter as ctk

from gui import efektler, tema
from gui.giris_ekrani import GirisEkrani
from gui.masa import Masa
from gui.yapim_asamasinda import YapimAsamasinda

# anahtar: (ekran başlığı, ekranı hazırlayacak üye)
# Bir üye kendi ekranını yazınca sayfa_ac() içinde buraya bağlanır.
SAYFALAR = {
    "kisiler": ("Şahıs Arşivi", "Deniz Acar"),
    "vaka_detay": ("Vaka Dosyası", "AhmetRasimVural"),
    "iliski_panosu": ("İlişki Panosu", "AhmetRasimVural"),
    "zaman_cizelgesi": ("Zaman Çizelgesi", "Xavnetex"),
    "analiz": ("Şüphe Analizi", "Xavnetex"),
    "yeni_vaka": ("Yeni Vaka Kaydı", "Xavnetex"),
}


class AnaPencere(ctk.CTk):
    def __init__(self, vt=None):
        super().__init__()
        self.vt = vt
        self.dedektif = None   # (id, ad, soyad, sicil_no) — giriş yapınca dolar
        self.ses = efektler.Ses()
        self.ekran = None

        ctk.set_appearance_mode("dark")
        self.title("Dedektif Bürosu — Vaka Yönetim Sistemi")
        self.geometry("1280x760")
        self.minsize(1000, 620)
        self.configure(fg_color=tema.RENKLER["masa"])
        self.after(0, self._tam_ekran)

        self.giris_ekrani_goster()

    def _tam_ekran(self):
        try:
            self.state("zoomed")   # Windows'ta pencereyi büyütür
        except Exception:
            pass

    def _ekran_degistir(self, yeni_ekran):
        if self.ekran is not None:
            self.ekran.destroy()
        self.ekran = yeni_ekran
        self.ekran.pack(fill="both", expand=True)

    def giris_ekrani_goster(self):
        self._ekran_degistir(GirisEkrani(self, self))

    def giris_yap(self, dedektif):
        self.dedektif = dedektif
        self.masaya_don()

    def cikis(self):
        self.dedektif = None
        self.ses.cal("kagit")
        self.giris_ekrani_goster()

    def masaya_don(self):
        self.ses.cal("kagit")
        self._ekran_degistir(Masa(self, self))

    def sayfa_ac(self, anahtar, vaka_id=None):
        baslik, sorumlu = SAYFALAR[anahtar]
        self.ses.cal("kagit")
        self._ekran_degistir(YapimAsamasinda(self, self, baslik, sorumlu, vaka_id))
