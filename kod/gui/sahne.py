"""Masa temalı ekranların ortak taban sınıfı.

Her ekran 1280x720'lik bir "tasarım alanı" koordinatlarıyla çizilir;
pencere boyutu değişince her şey orantılı olarak yeniden çizilir.
"""
import tkinter as tk

import customtkinter as ctk
from PIL import Image, ImageTk

from gui import dokular, tema

TASARIM_W, TASARIM_H = 1280, 720
UST_BANT = 48


class Sahne(ctk.CTkFrame):
    ust_bant_var = True

    def __init__(self, master, uygulama):
        super().__init__(master, fg_color=tema.RENKLER["masa"], corner_radius=0)
        self.uyg = uygulama
        self.resimler = []
        self._bekleyen_cizim = None
        self.s, self.ox, self.oy = 1.0, 0.0, 0.0

        self.canvas = tk.Canvas(self, highlightthickness=0, bg=tema.RENKLER["masa"])
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self._boyut_degisti)

    # --- çizim döngüsü -------------------------------------------------
    def _boyut_degisti(self, _olay):
        if self._bekleyen_cizim:
            self.after_cancel(self._bekleyen_cizim)
        self._bekleyen_cizim = self.after(60, self.yeniden_ciz)

    def yeniden_ciz(self):
        self._bekleyen_cizim = None
        c = self.canvas
        W, H = c.winfo_width(), c.winfo_height()
        if W < 50 or H < 50:
            return
        c.delete("all")
        self.resimler.clear()
        c.efekt_resimleri = []

        ust = UST_BANT if self.ust_bant_var else 0
        self.W, self.H = W, H
        self.s = min(W / TASARIM_W, (H - ust) / TASARIM_H)
        self.ox = (W - TASARIM_W * self.s) / 2
        self.oy = ust + (H - ust - TASARIM_H * self.s) / 2

        self.resim_px(dokular.masa(W, H), 0, 0)
        self.ciz()

    def ciz(self):
        """Alt sınıflar sahneyi burada çizer."""
        raise NotImplementedError

    # --- koordinat yardımcıları -----------------------------------------
    def P(self, x, y):
        """Tasarım koordinatını ekran pikseline çevirir."""
        return self.ox + x * self.s, self.oy + y * self.s

    def K(self, *xy):
        """Birden çok (x, y) çiftini çevirir: K(x1, y1, x2, y2...)."""
        sonuc = []
        for i in range(0, len(xy), 2):
            sonuc.extend(self.P(xy[i], xy[i + 1]))
        return sonuc

    def px(self, deger):
        return max(1, round(deger * self.s))

    def wpx(self, deger):
        """CustomTkinter widget boyutu: ekran ölçeği (DPI) payı düşülmüş px()."""
        try:
            olcek = ctk.ScalingTracker.get_widget_scaling(self)
        except Exception:
            olcek = 1.0
        return max(1, round(deger * self.s / olcek))

    def F(self, boyut, kalin=False, aile=tema.DAKTILO):
        """Ölçeklenmiş canvas yazı tipi (negatif boyut = piksel)."""
        return (aile, -max(7, round(boyut * self.s)), "bold" if kalin else "normal")

    # --- görüntü yardımcıları -------------------------------------------
    def resim_px(self, img, x, y, anchor="nw", tags=()):
        foto = ImageTk.PhotoImage(img)
        self.resimler.append(foto)
        return self.canvas.create_image(x, y, image=foto, anchor=anchor, tags=tags)

    def resim(self, img, x, y, anchor="nw", tags=()):
        return self.resim_px(img, *self.P(x, y), anchor=anchor, tags=tags)

    def kagit(self, x1, y1, x2, y2, ton="krem", tags=(), golge=True):
        """Tasarım koordinatlarında dokulu bir kâğıt parçası çizer."""
        if golge:
            self.canvas.create_rectangle(*self.K(x1 + 5, y1 + 7, x2 + 5, y2 + 7),
                                         fill=tema.RENKLER["masa_golge"], outline="")
        img = dokular.kagit(self.px(x2 - x1), self.px(y2 - y1), ton)
        return self.resim(img, x1, y1, tags=tags)

    def golgeli_resim(self, img, x, y, tags=()):
        """RGBA görüntüyü yumuşak gölgesiyle birlikte koyar (piksel konumu)."""
        golge, pay = dokular.golge(img, max(3, self.px(8)))
        self.resim_px(golge, x + self.px(6) - pay, y + self.px(8) - pay)
        return self.resim_px(img, x, y, tags=tags)

    def yuvarlak_dikdortgen(self, x1, y1, x2, y2, r, **secenekler):
        noktalar = [x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r, x2, y2,
                    x2 - r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1]
        return self.canvas.create_polygon(*self.K(*noktalar), smooth=True, **secenekler)

    # --- etkileşim ------------------------------------------------------
    def tiklanabilir(self, tag, x1, y1, x2, y2, ipucu, eylem, kaldir=True):
        """Bir nesne grubunu üzerine gelince kalkan, tıklanınca eylem yapan hâle getirir.

        Nesnenin üstüne görünmez bir 'tıklama alanı' konur; nesne hareket etse de
        alan sabit kalır, böylece fare titremesi olmaz.
        """
        (ax1, ay1), (ax2, ay2) = self.P(x1, y1), self.P(x2, y2)
        bos = Image.new("RGBA", (max(1, int(ax2 - ax1)), max(1, int(ay2 - ay1))), (0, 0, 0, 0))
        alan = self.resim_px(bos, ax1, ay1)
        kalkis = self.px(4) if kaldir else 0

        def giris(_):
            self.canvas.move(tag, 0, -kalkis)
            self.canvas.configure(cursor="hand2")
            self.ipucu_goster(ipucu)

        def cikis(_):
            self.canvas.move(tag, 0, kalkis)
            self.canvas.configure(cursor="")
            self.ipucu_goster(None)

        self.canvas.tag_bind(alan, "<Enter>", giris)
        self.canvas.tag_bind(alan, "<Leave>", cikis)
        self.canvas.tag_bind(alan, "<Button-1>", lambda _: eylem())
        return alan

    def ipucu_goster(self, metin):
        """Alt sınıflar isterse ipucunu bir yerde gösterir."""

    # --- üst bant -------------------------------------------------------
    def ust_bant_ciz(self, alt_baslik):
        c, W = self.canvas, self.W
        c.create_rectangle(0, 0, W, UST_BANT, fill=tema.RENKLER["ust_bant"], outline="")
        c.create_line(0, UST_BANT - 1, W, UST_BANT - 1, fill=tema.RENKLER["pirinc"], width=2)
        baslik = c.create_text(20, UST_BANT / 2, text="DEDEKTİF BÜROSU", anchor="w",
                               font=(tema.DAKTILO, -19, "bold"), fill=tema.RENKLER["acik_metin"])
        sag = c.bbox(baslik)[2]
        alt = c.create_text(sag + 12, UST_BANT / 2, text=f"·  {alt_baslik}", anchor="w",
                            font=(tema.DAKTILO, -14), fill=tema.RENKLER["soluk_metin"])
        return c.bbox(alt)[2]

    def yazi_dugmesi(self, x, y, metin, eylem, anchor="e", boyut=14):
        """Üzerine gelince parlayan, tıklanabilir yazı (piksel konumu). Öğe kimliğini döndürür."""
        c = self.canvas
        oge = c.create_text(x, y, text=metin, anchor=anchor,
                            font=(tema.DAKTILO, -boyut, "bold"), fill=tema.RENKLER["pirinc"])
        c.tag_bind(oge, "<Enter>", lambda _: (c.itemconfigure(oge, fill=tema.RENKLER["acik_metin"]),
                                              c.configure(cursor="hand2")))
        c.tag_bind(oge, "<Leave>", lambda _: (c.itemconfigure(oge, fill=tema.RENKLER["pirinc"]),
                                              c.configure(cursor="")))
        c.tag_bind(oge, "<Button-1>", lambda _: eylem())
        return oge

    def ust_bant_dugmesi(self, x, metin, eylem):
        """Üst bantın sağındaki tıklanabilir yazı. Sol kenarının x'ini döndürür."""
        oge = self.yazi_dugmesi(x, UST_BANT / 2, metin, eylem)
        return self.canvas.bbox(oge)[0]
