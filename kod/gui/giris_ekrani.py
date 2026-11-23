"""Dedektif giriş ekranı: masanın üstünde bir personel kimlik kartı.

Sicil numarası girilir; VeriTabani.dedektif_bul(sicil_no) dedektifi bulursa
karta ad yazılır, "ONAYLANDI" damgası basılır ve masaya geçilir.
"""
from tkinter import messagebox

import customtkinter as ctk

from gui import dokular, efektler, tema
from gui.sahne import Sahne

KART_W, KART_H = 600, 340


class GirisEkrani(Sahne):
    ust_bant_var = False

    def __init__(self, master, uygulama):
        super().__init__(master, uygulama)
        self.mesgul = False
        self.durum_metni = ""

        kagit = tema.RENKLER["kagit"]
        self.sicil_girdisi = ctk.CTkEntry(
            self.canvas, width=220, height=38, corner_radius=4, border_width=2,
            fg_color="#f5eedb", border_color="#8a7f63", bg_color=kagit,
            text_color=tema.RENKLER["murekkep"], placeholder_text="D-0000",
            placeholder_text_color="#a39a82", font=(tema.DAKTILO, 18, "bold"),
        )
        self.sicil_girdisi.bind("<Return>", lambda _: self.giris_yap())
        self.giris_dugmesi = ctk.CTkButton(
            self.canvas, text="GİRİŞ  ▸", width=150, height=38, corner_radius=4,
            fg_color=tema.RENKLER["kirmizi"], hover_color=tema.RENKLER["kirmizi_hover"],
            bg_color=kagit, text_color="#f5eedb", font=(tema.DAKTILO, 16, "bold"),
            command=self.giris_yap,
        )
        self.after(300, self.sicil_girdisi.focus_set)

    def ciz(self):
        c = self.canvas
        cx, cy = self.W / 2, self.H / 2 + 20
        x1, y1 = cx - KART_W / 2, cy - KART_H / 2
        self.kart_konumu = (x1, y1)

        c.create_text(cx, y1 - 92, text="DEDEKTİF BÜROSU", font=(tema.DAKTILO, -40, "bold"),
                      fill=tema.RENKLER["acik_metin"])
        c.create_text(cx, y1 - 52, text="— PERSONEL GİRİŞİ —", font=(tema.DAKTILO, -16),
                      fill=tema.RENKLER["soluk_metin"])

        self.golgeli_resim(dokular.kimlik_karti(KART_W, KART_H), x1, y1, tags=("kart",))
        sol = x1 + 24 + int(KART_W * 0.25) + 28
        self.ad_ogesi = c.create_text(sol + 4, y1 + int(KART_H * 0.14) + 64, anchor="sw", text="",
                                      font=(tema.DAKTILO, -20, "bold"), fill=tema.RENKLER["mavi_murekkep"],
                                      tags=("kart",))
        c.create_window(sol, y1 + KART_H * 0.14 + 108, window=self.sicil_girdisi, anchor="nw", tags=("kart",))
        c.create_window(sol + 232, y1 + KART_H * 0.14 + 108, window=self.giris_dugmesi, anchor="nw", tags=("kart",))
        self.durum_ogesi = c.create_text(sol, y1 + KART_H * 0.14 + 160, anchor="nw", width=KART_W - (sol - x1) - 20,
                                         text=self.durum_metni, font=(tema.DAKTILO, -13, "bold"),
                                         fill=tema.RENKLER["kirmizi"], tags=("kart",))

        if self.uyg.vt is None:
            self._durum("Veri tabanı bağlı değil. VeriTabani sınıfı yazılınca giriş açılacak.")
            self.yazi_dugmesi(cx, y1 + KART_H + 40, "Bağlantısız devam et  ▸",
                              lambda: self.uyg.giris_yap(None), anchor="center")
        else:
            c.create_text(cx, y1 + KART_H + 40, text="Örnek sicil numarası: D-1042",
                          font=(tema.DAKTILO, -13), fill=tema.RENKLER["soluk_metin"])

    def _durum(self, metin, renk=None):
        self.durum_metni = metin
        self.canvas.itemconfigure(self.durum_ogesi, text=metin, fill=renk or tema.RENKLER["kirmizi"])

    def giris_yap(self):
        if self.mesgul:
            return
        sicil = self.sicil_girdisi.get().strip().upper()
        if not sicil:
            self._durum("Sicil numarası boş bırakılamaz.")
            efektler.titret(self.canvas, "kart")
            return
        if self.uyg.vt is None:
            self._durum("Veri tabanı bağlı değil; giriş yapılamıyor.")
            efektler.titret(self.canvas, "kart")
            return

        try:
            dedektif = self.uyg.vt.dedektif_bul(sicil)
        except Exception as hata:
            messagebox.showerror("Veri tabanı hatası", f"Dedektif bilgisi okunamadı:\n{hata}")
            return

        if dedektif is None:
            self._durum(f"'{sicil}' sicil numarasıyla kayıtlı dedektif bulunamadı.")
            efektler.titret(self.canvas, "kart")
            return

        self.mesgul = True
        self.giris_dugmesi.configure(state="disabled")
        self._durum("Kimlik doğrulandı.", tema.RENKLER["yesil"])
        _, ad, soyad, _ = dedektif
        efektler.daktilo_yaz(self.canvas, self.ad_ogesi, f"{ad} {soyad}".upper(), hiz=45,
                             ses=self.uyg.ses, bitince=lambda: self._onayla(dedektif))

    def _onayla(self, dedektif):
        x1, y1 = self.kart_konumu
        efektler.damga_bas(self.canvas, x1 + 24 + KART_W * 0.125, y1 + KART_H * 0.5, "ONAYLANDI",
                           tema.RENKLER["yesil"], 26, aci=14, ses=self.uyg.ses, tags=("kart",),
                           bitince=lambda _: self.after(900, lambda: self.uyg.giris_yap(dedektif)))
