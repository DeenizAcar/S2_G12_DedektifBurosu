"""Ana ekran: dedektifin masası.

Masadaki her nesne bir ekrana açılır:
  şahıs arşivi -> Kişiler          vaka dosyaları -> Vaka Dosyası
  daktilo      -> Yeni Vaka        mantar pano    -> İlişki Panosu
  not defteri  -> Analiz           teleks şeridi  -> Zaman Çizelgesi
  radyo        -> sesi aç/kapa     damga          -> küçük bir sürpriz

Veriler VeriTabani.dedektif_vakalari(dedektif_id) metodundan gelir:
  [(vaka_id, baslik, durum, olay_baslangic), ...]
"""
import random
from datetime import date
from tkinter import messagebox

from gui import dokular, efektler, tema
from gui.sahne import UST_BANT, Sahne

DURUMLAR = ("Açık", "Soruşturmada", "Çözüldü", "Kapandı")
MASADA_EN_FAZLA = 4


def tarih_bicimle(metin):
    """'2026-11-14 21:00' -> '14.11.2026'"""
    try:
        yil, ay, gun = metin[:10].split("-")
        return f"{gun}.{ay}.{yil}"
    except (ValueError, TypeError):
        return metin or "—"


class Masa(Sahne):
    def __init__(self, master, uygulama):
        super().__init__(master, uygulama)
        self.vakalar = self._vakalari_oku()

    def _vakalari_oku(self):
        vt, dedektif = self.uyg.vt, self.uyg.dedektif
        if vt is None or dedektif is None:
            return []
        try:
            return list(vt.dedektif_vakalari(dedektif[0]))
        except Exception as hata:
            messagebox.showerror("Veri tabanı hatası", f"Vakalar okunamadı:\n{hata}")
            return []

    # ------------------------------------------------------------------
    def ciz(self):
        self._ust_bant()
        self._sahis_arsivi()
        self._durum_raporu()
        self._vaka_dosyalari()
        self._teleks()
        self._daktilo()
        self._pano()
        self._not_defteri()
        self._kahve()
        self._damga_seti()
        self._radyo()

    def ipucu_goster(self, metin):
        self.canvas.itemconfigure(self.ipucu_ogesi, text=f"▸ {metin}" if metin else "Bir nesneye tıklayın")

    def _ust_bant(self):
        baslik_sonu = self.ust_bant_ciz("VAKA MASASI")
        c = self.canvas
        sol = self.ust_bant_dugmesi(self.W - 20, "[ ÇIKIŞ ]", self.uyg.cikis)

        dedektif = self.uyg.dedektif
        if dedektif is None:
            kimlik = "BAĞLANTISIZ MOD"
        elif self.W >= 1200:
            kimlik = f"{dedektif[1]} {dedektif[2]}  ·  SİCİL {dedektif[3]}  ·  {date.today():%d.%m.%Y}"
        else:
            kimlik = f"{dedektif[1]} {dedektif[2]}  ·  {dedektif[3]}"
        bilgi = c.create_text(sol - 24, UST_BANT / 2, anchor="e", font=(tema.DAKTILO, -13),
                              text=kimlik.upper(), fill=tema.RENKLER["soluk_metin"])

        # ipucu, başlık ile dedektif bilgisi arasındaki boşluğun ortasında durur
        orta = (baslik_sonu + c.bbox(bilgi)[0]) / 2
        self.ipucu_ogesi = c.create_text(orta, UST_BANT / 2, text="Bir nesneye tıklayın",
                                         font=(tema.DAKTILO, -13, "bold"), fill=tema.RENKLER["acik_metin"])

    # --- sol: şahıs arşivi ve durum raporu --------------------------------
    def _sahis_arsivi(self):
        c, t = self.canvas, "arsiv"
        c.create_rectangle(*self.K(37, 38, 257, 338), fill=tema.RENKLER["masa_golge"], outline="")
        c.create_rectangle(*self.K(30, 30, 250, 330), fill=tema.RENKLER["metal"],
                           outline=tema.RENKLER["metal_koyu"], width=self.px(2), tags=t)
        c.create_rectangle(*self.K(44, 62, 236, 318), fill="#2f332c", outline="", tags=t)

        harfler = "A Ç F İ L N Ş U Z".split()
        for i, harf in enumerate(harfler):
            y = 72 + i * 27
            renk = "#e6dcc0" if i % 2 else "#dcd1b1"
            sekme_x = 58 + (i % 3) * 58
            c.create_rectangle(*self.K(sekme_x, y - 8, sekme_x + 34, y + 2), fill=renk, outline="#a89c7c", tags=t)
            c.create_rectangle(*self.K(52, y, 228, y + 24), fill=renk, outline="#a89c7c", tags=t)
            c.create_text(*self.P(sekme_x + 17, y - 3), text=harf, font=self.F(8, True),
                          fill=tema.RENKLER["soluk_murekkep"], tags=t)

        c.create_rectangle(*self.K(85, 37, 195, 56), fill=tema.RENKLER["pirinc"],
                           outline=tema.RENKLER["pirinc_koyu"], tags=t)
        c.create_text(*self.P(140, 46.5), text="ŞAHIS ARŞİVİ", font=self.F(10, True), fill="#2a2112", tags=t)
        self.tiklanabilir(t, 30, 30, 250, 330, "Şahıs arşivi: şüpheli ve tanık kartları",
                          lambda: self.uyg.sayfa_ac("kisiler"))

    def _durum_raporu(self):
        c = self.canvas
        self.kagit(36, 362, 246, 692)
        c.create_text(*self.P(52, 378), anchor="nw", text="GÜNLÜK DURUM RAPORU",
                      font=self.F(12, True), fill=tema.RENKLER["murekkep"])
        c.create_line(*self.K(52, 400, 230, 400), fill=tema.RENKLER["murekkep"])
        c.create_text(*self.P(52, 408), anchor="nw", text=f"TARİH: {date.today():%d.%m.%Y}",
                      font=self.F(10), fill=tema.RENKLER["soluk_murekkep"])

        bagli = self.uyg.dedektif is not None
        for i, durum in enumerate(DURUMLAR):
            y = 446 + i * 36
            sayi = sum(1 for v in self.vakalar if v[2] == durum) if bagli else "–"
            c.create_oval(*self.K(52, y - 5, 62, y + 5), fill=tema.DURUM_RENKLERI[durum], outline="")
            c.create_text(*self.P(70, y), anchor="w", text=f"{durum.upper():.<14}{sayi:>3}",
                          font=self.F(11), fill=tema.RENKLER["murekkep"])

        c.create_line(*self.K(52, 592, 230, 592), fill=tema.RENKLER["murekkep"], dash=(2, 3))
        toplam = len(self.vakalar) if bagli else "–"
        c.create_text(*self.P(52, 610), anchor="nw", text=f"TOPLAM DOSYA: {toplam}",
                      font=self.F(11, True), fill=tema.RENKLER["murekkep"])
        self.resim(dokular.damga("ARŞİV", tema.rgb(tema.RENKLER["mavi_murekkep"]), self.px(13), -8),
                   150, 640)

    # --- orta: gelen evrak ve teleks ---------------------------------------
    def _vaka_dosyalari(self):
        c = self.canvas
        c.create_rectangle(*self.K(275, 22, 805, 562), fill="#30352d", outline="#22261f", width=self.px(3))
        c.create_rectangle(*self.K(287, 34, 793, 550), fill="", outline="#474d41", width=self.px(1))
        c.create_rectangle(*self.K(470, 553, 610, 573), fill=tema.RENKLER["pirinc"],
                           outline=tema.RENKLER["pirinc_koyu"])
        c.create_text(*self.P(540, 563), text="GELEN EVRAK", font=self.F(10, True), fill="#2a2112")

        if not self.vakalar:
            neden = ("Daktilodan yeni vaka açabilirsiniz." if self.uyg.dedektif
                     else "Giriş yapılmadığı için dosya gösterilmiyor.")
            c.create_text(*self.P(540, 270), text="DOSYA YOK", font=self.F(26, True), fill="#4f5648")
            c.create_text(*self.P(540, 310), text=neden, font=self.F(12), fill="#7b8272")
            return

        kaymalar = (0, 22, -6, 14)
        acilar = (-1.8, 1.2, -0.8, 2.0)
        for i, (vaka_id, baslik, durum, tarih) in enumerate(self.vakalar[:MASADA_EN_FAZLA]):
            x, y = 300 + kaymalar[i], 40 + i * 112
            img = dokular.klasor(self.px(440), self.px(116), vaka_id, baslik, tarih_bicimle(tarih), durum,
                                 tema.rgb(tema.DURUM_RENKLERI.get(durum, "#4d5156")), acilar[i])
            t = f"vaka{vaka_id}"
            self.golgeli_resim(img, *self.P(x, y), tags=t)
            self.tiklanabilir(t, x, y, x + img.width / self.s, y + img.height / self.s,
                              f"Vaka {vaka_id:04d}: {baslik}",
                              lambda v=vaka_id: self.uyg.sayfa_ac("vaka_detay", vaka_id=v))

        kalan = len(self.vakalar) - MASADA_EN_FAZLA
        if kalan > 0:
            c.create_text(*self.P(780, 535), anchor="e", text=f"+ {kalan} dosya daha",
                          font=self.F(11, True), fill=tema.RENKLER["acik_metin"])

    def _teleks(self):
        c, t = self.canvas, "teleks"
        self.kagit(280, 592, 800, 690, tags=t)
        for x in range(292, 796, 16):
            c.create_oval(*self.K(x - 2, 598, x + 2, 602), fill="#8a8370", outline="", tags=t)
            c.create_oval(*self.K(x - 2, 680, x + 2, 684), fill="#8a8370", outline="", tags=t)
        c.create_text(*self.P(300, 612), anchor="w", text="TELEKS  ▸  ZAMAN ÇİZELGESİ",
                      font=self.F(11, True), fill=tema.RENKLER["murekkep"], tags=t)
        c.create_line(*self.K(300, 664, 780, 664), fill=tema.RENKLER["murekkep"], tags=t)
        for k in range(6):
            x = 300 + k * 96
            c.create_line(*self.K(x, 660, x, 668), fill=tema.RENKLER["murekkep"], tags=t)
            c.create_text(*self.P(x, 674), text=f"{19 + k}:00", font=self.F(8),
                          fill=tema.RENKLER["soluk_murekkep"], tags=t)
        for x1, x2, y, renk in ((330, 470, 636, "#4a6a8a"), (410, 560, 646, "#6a7d4e"), (520, 640, 654, "#7b6a8a")):
            c.create_rectangle(*self.K(x1, y - 3, x2, y + 3), fill=renk, outline="", tags=t)
        c.create_oval(*self.K(523, 642, 533, 652), fill=tema.RENKLER["kirmizi"], outline="", tags=t)
        self.tiklanabilir(t, 280, 592, 800, 690, "Teleks: olayların ve alibilerin zaman çizelgesi",
                          lambda: self.uyg.sayfa_ac("zaman_cizelgesi"))

    # --- sağ: daktilo, pano, not defteri, kahve, damga, radyo --------------
    def _daktilo(self):
        c, t = self.canvas, "daktilo"
        self.kagit(885, 12, 1005, 108, tags=t, golge=False)
        c.create_text(*self.P(945, 52), text="YENİ VAKA\nKAYDI", justify="center",
                      font=self.F(12, True), fill=tema.RENKLER["murekkep"], tags=t)
        c.create_rectangle(*self.K(854, 102, 1060, 310), fill=tema.RENKLER["masa_golge"], outline="")
        self.yuvarlak_dikdortgen(846, 98, 1044, 300, 18, fill="#4b6656", outline="#2c3d33",
                                 width=self.px(2), tags=t)
        c.create_rectangle(*self.K(836, 80, 1054, 104), fill="#22261f", outline="#111", tags=t)
        for x in (828, 1062):
            c.create_oval(*self.K(x - 10, 82, x + 10, 102), fill="#151815", outline="#000", tags=t)
        c.create_rectangle(*self.K(870, 108, 1020, 116), fill="#1a1d18", outline="", tags=t)

        for sira, adet in enumerate((10, 9, 8)):
            y = 150 + sira * 30
            bas = 945 - (adet - 1) * 18 / 2
            for k in range(adet):
                x = bas + k * 18
                c.create_oval(*self.K(x - 7, y - 7, x + 7, y + 7), fill="#e9e1c9", outline="#1d1d1d", tags=t)
        self.yuvarlak_dikdortgen(900, 236, 990, 250, 6, fill="#e9e1c9", outline="#1d1d1d", tags=t)
        c.create_rectangle(*self.K(918, 266, 972, 284), fill=tema.RENKLER["pirinc"],
                           outline=tema.RENKLER["pirinc_koyu"], tags=t)
        c.create_text(*self.P(945, 275), text="BÜRO-7", font=self.F(9, True), fill="#2a2112", tags=t)
        self.tiklanabilir(t, 822, 12, 1068, 310, "Daktilo: yeni vaka aç",
                          lambda: self.uyg.sayfa_ac("yeni_vaka"))

    def _pano(self):
        c, t = self.canvas, "pano"
        c.create_rectangle(*self.K(1082, 23, 1267, 338), fill=tema.RENKLER["masa_golge"], outline="")
        c.create_rectangle(*self.K(1075, 15, 1260, 330), fill="#6b4a2b", outline="#3e2a17",
                           width=self.px(2), tags=t)
        self.resim(dokular.kagit(self.px(161), self.px(291), "mantar"), 1087, 27, tags=t)

        fotolar = ((1100, 45, 1150, 105), (1185, 58, 1235, 118), (1104, 190, 1154, 250), (1180, 212, 1230, 272))
        for x1, y1, x2, y2 in fotolar:
            c.create_rectangle(*self.K(x1, y1, x2, y2), fill="#f1eee6", outline="#bdb6a5", tags=t)
            self.resim(dokular.siluet(self.px(x2 - x1 - 10), self.px(y2 - y1 - 20)), x1 + 5, y1 + 5, tags=t)
        self.kagit(1136, 138, 1196, 172, tags=t, golge=False)
        c.create_text(*self.P(1166, 155), text="?", font=self.F(16, True), fill=tema.RENKLER["kirmizi"], tags=t)

        igneler = [((x1 + x2) / 2, y1 + 4) for x1, y1, x2, y2 in fotolar] + [(1166, 142)]
        for a, b in ((0, 1), (0, 2), (1, 3), (2, 3), (1, 4), (2, 4)):
            c.create_line(*self.K(*igneler[a], *igneler[b]), fill="#c0392b", width=self.px(2), tags=t)
        for x, y in igneler:
            c.create_oval(*self.K(x - 4, y - 4, x + 4, y + 4), fill="#d4392f", outline="#7a1a12", tags=t)

        self.kagit(1112, 292, 1222, 314, tags=t, golge=False)
        c.create_text(*self.P(1167, 303), text="İLİŞKİ PANOSU", font=self.F(9, True),
                      fill=tema.RENKLER["murekkep"], tags=t)
        self.tiklanabilir(t, 1075, 15, 1260, 330, "Mantar pano: şüpheli-delil ilişki ağı",
                          lambda: self.uyg.sayfa_ac("iliski_panosu"))

    def _not_defteri(self):
        c, t = self.canvas, "defter"
        self.kagit(872, 345, 1047, 585, ton="beyaz", tags=t)
        for y in range(385, 580, 20):
            c.create_line(*self.K(872, y, 1047, y), fill="#9db4cc", tags=t)
        c.create_line(*self.K(902, 345, 902, 585), fill="#d98c8c", tags=t)
        for y in range(360, 580, 20):
            c.create_oval(*self.K(862, y - 5, 880, y + 5), outline="#555a52", width=self.px(2), tags=t)

        murekkep = tema.RENKLER["mavi_murekkep"]
        c.create_text(*self.P(912, 368), anchor="w", text="Şüpheliler", font=self.F(15, True, tema.EL_YAZISI),
                      fill=murekkep, tags=t)
        for i, satir in enumerate(("kim?", "nerede?", "ne zaman?", "neden?")):
            c.create_text(*self.P(916, 396 + i * 40), anchor="w", text=satir,
                          font=self.F(13, False, tema.EL_YAZISI), fill=murekkep, tags=t)
        c.create_oval(*self.K(906, 382, 962, 410), outline=tema.RENKLER["kirmizi"], width=self.px(2), tags=t)
        self.tiklanabilir(t, 860, 345, 1047, 585, "Not defteri: şüphe analizi",
                          lambda: self.uyg.sayfa_ac("analiz"))

    def _kahve(self):
        c = self.canvas
        c.create_oval(*self.K(806, 618, 862, 674), outline="#2f3529", width=self.px(3))
        c.create_oval(*self.K(1112, 362, 1212, 456), fill=tema.RENKLER["masa_golge"], outline="")
        c.create_oval(*self.K(1104, 354, 1196, 446), fill="#d8d0bf", outline="#a79f8d")
        c.create_oval(*self.K(1178, 391, 1202, 409), fill="#efe9dc", outline="#b5ad9a", width=self.px(2))
        c.create_oval(*self.K(1116, 366, 1184, 434), fill="#efe9dc", outline="#b5ad9a", width=self.px(2))
        c.create_oval(*self.K(1124, 374, 1176, 426), fill="#3a2314", outline="#6b4528", width=self.px(2))
        c.create_oval(*self.K(1136, 384, 1146, 391), fill="#5a3a24", outline="")

    def _damga_seti(self):
        c, t = self.canvas, "damga"
        c.create_rectangle(*self.K(1078, 478, 1158, 526), fill="#2a2a2a", outline="#111")
        c.create_rectangle(*self.K(1084, 484, 1152, 520), fill="#7a1f1a", outline="")
        c.create_rectangle(*self.K(1186, 506, 1238, 518), fill="#3a2a1a", outline="#1a120a", tags=t)
        c.create_oval(*self.K(1197, 476, 1227, 506), fill="#8b5a2b", outline="#4a2f15", width=self.px(2), tags=t)
        self.tiklanabilir(t, 1180, 470, 1244, 522, "Damga: bir şey damgala", self._sakaci_damga)

    def _sakaci_damga(self):
        x, y = self.P(random.randint(330, 760), random.randint(120, 480))
        metin = random.choice(("GİZLİ", "ACİL", "İNCELENDİ", "ARŞİVLENDİ"))
        efektler.damga_bas(self.canvas, x, y, metin, tema.RENKLER["kirmizi"], self.px(30),
                           aci=random.randint(-18, 18), ses=self.uyg.ses,
                           bitince=lambda oge: self.after(1400, lambda: self.canvas.delete(oge)))

    def _radyo(self):
        c, t = self.canvas, "radyo"
        c.create_rectangle(*self.K(1082, 598, 1267, 713), fill=tema.RENKLER["masa_golge"], outline="")
        self.yuvarlak_dikdortgen(1075, 590, 1260, 705, 12, fill="#5b3b25", outline="#2e1d10",
                                 width=self.px(2), tags=t)
        c.create_rectangle(*self.K(1088, 602, 1170, 693), fill="#3a2616", outline="", tags=t)
        for x in range(1094, 1168, 9):
            for y in range(608, 690, 9):
                c.create_oval(*self.K(x, y, x + 4, y + 4), fill="#20140b", outline="", tags=t)
        c.create_oval(*self.K(1191, 611, 1239, 659), fill="#e6dcc0", outline="#2e1d10", width=self.px(2), tags=t)
        self.ibre = c.create_line(*self.K(1215, 635, 1215, 615), fill=tema.RENKLER["kirmizi"],
                                  width=self.px(2), tags=t)
        self.radyo_yazisi = c.create_text(*self.P(1215, 682), text="", font=self.F(10, True),
                                          fill="#e6dcc0", tags=t)
        self._radyo_guncelle()
        self.tiklanabilir(t, 1075, 590, 1260, 705, "Radyo: sesi aç / kapat", self._ses_degistir)

    def _ses_degistir(self):
        self.uyg.ses.acik = not self.uyg.ses.acik
        self.uyg.ses.cal("daktilo")
        self._radyo_guncelle()

    def _radyo_guncelle(self):
        acik = self.uyg.ses.acik
        # radyo üzerine gelinince yukarı kalktığı için ibrenin o anki merkezi kullanılır
        mx, my = self.canvas.coords(self.ibre)[:2]
        yon = 1 if acik else -1
        uzunluk = self.px(14)
        self.canvas.coords(self.ibre, mx, my, mx + yon * uzunluk, my - uzunluk)
        self.canvas.itemconfigure(self.radyo_yazisi, text="SES: AÇIK" if acik else "SES: KAPALI")
