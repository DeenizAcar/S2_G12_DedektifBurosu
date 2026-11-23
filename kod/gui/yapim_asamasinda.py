"""Henüz yazılmamış ekranlar için geçici sayfa: masaya bırakılmış bir iç yazışma.

Her üye kendi ekranını yazınca ana_pencere.py'deki SAYFALAR sözlüğünde
bu sınıfın yerine kendi sınıfını koyar.
"""
from gui import dokular, efektler, tema
from gui.sahne import Sahne


class YapimAsamasinda(Sahne):
    def __init__(self, master, uygulama, baslik, sorumlu, vaka_id=None):
        super().__init__(master, uygulama)
        self.baslik = baslik
        self.sorumlu = sorumlu
        self.vaka_id = vaka_id
        self.animasyon_yapildi = False

    def ciz(self):
        c = self.canvas
        self.ust_bant_ciz(self.baslik.upper())
        self.ust_bant_dugmesi(self.W - 20, "[ ◂ MASAYA DÖN ]", self.uyg.masaya_don)

        self.kagit(340, 40, 940, 690)
        murekkep = tema.RENKLER["murekkep"]
        c.create_text(*self.P(380, 80), anchor="nw", text="DEDEKTİF BÜROSU  ·  İÇ YAZIŞMA",
                      font=self.F(13, True), fill=murekkep)
        c.create_line(*self.K(380, 108, 900, 108), fill=murekkep, width=self.px(2))

        satirlar = [f"KONU   : {self.baslik.upper()}", f"SORUMLU: {self.sorumlu}"]
        if self.vaka_id is not None:
            satirlar.append(f"DOSYA  : VAKA {self.vaka_id:04d}")
        govde = "\n".join(satirlar) + (
            "\n\nBu ekran henüz yapım aşamasındadır.\n"
            "Model sınıfları tamamlandığında\n"
            "burada gerçek kayıtlar görünecektir.\n\n"
            "Gereği rica olunur."
        )
        yazi = c.create_text(*self.P(380, 140), anchor="nw", text="", font=self.F(15), fill=murekkep)

        if self.animasyon_yapildi:
            c.itemconfigure(yazi, text=govde)
            self._damga(animasyonlu=False)
        else:
            self.animasyon_yapildi = True
            efektler.daktilo_yaz(c, yazi, govde, hiz=10, ses=self.uyg.ses, bitince=self._damga)

    def _damga(self, animasyonlu=True):
        x, y = self.P(760, 590)
        if animasyonlu:
            efektler.damga_bas(self.canvas, x, y, "TASLAK", tema.RENKLER["kirmizi"], self.px(34),
                               aci=-14, ses=self.uyg.ses)
        else:
            self.resim_px(dokular.damga("TASLAK", tema.rgb(tema.RENKLER["kirmizi"]), self.px(34), -14),
                          x, y, anchor="center")
