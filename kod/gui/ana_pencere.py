"""Ana pencere: sol menü + sayfalar arası geçiş, ve Ana Panel ekranı.

GUI içinde SQL veya iş mantığı yoktur; veriler VeriTabani nesnesinin
(vt) metotlarından istenir.
"""
from tkinter import messagebox, ttk

import customtkinter as ctk

from gui import tema

# (anahtar, menüde görünen ad, ekranı hazırlayacak üye)
SAYFA_TANIMLARI = [
    ("ana_panel", "Ana Panel", "Deniz Acar"),
    ("kisiler", "Kişiler", "Deniz Acar"),
    ("vaka_detay", "Vaka Detayı", "AhmetRasimVural"),
    ("iliski_panosu", "İlişki Panosu", "AhmetRasimVural"),
    ("zaman_cizelgesi", "Zaman Çizelgesi", "Xavnetex"),
    ("analiz", "Analiz", "Xavnetex"),
]


class AnaPencere(ctk.CTk):
    def __init__(self, vt=None):
        super().__init__()
        self.vt = vt
        self.sayfalar = {}
        self.menu_butonlari = {}

        ctk.set_appearance_mode("dark")
        self.title("Dedektif Bürosu — Vaka Yönetim Sistemi")
        self.geometry("1200x720")
        self.minsize(1000, 600)
        self.configure(fg_color=tema.RENKLER["arka_plan"])

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._kenar_cubugu_olustur()

        self.icerik = ctk.CTkFrame(self, fg_color="transparent")
        self.icerik.grid(row=0, column=1, sticky="nsew", padx=28, pady=24)
        self.icerik.grid_rowconfigure(0, weight=1)
        self.icerik.grid_columnconfigure(0, weight=1)

        self.sayfa_goster("ana_panel")

    def _kenar_cubugu_olustur(self):
        cubuk = ctk.CTkFrame(self, width=230, corner_radius=0, fg_color=tema.RENKLER["kenar_cubugu"])
        cubuk.grid(row=0, column=0, sticky="nsw")
        cubuk.grid_propagate(False)
        cubuk.grid_columnconfigure(0, weight=1)

        ctk.CTkFrame(cubuk, height=4, corner_radius=0, fg_color=tema.RENKLER["vurgu"]).grid(
            row=0, column=0, sticky="ew"
        )
        ctk.CTkLabel(
            cubuk, text="DEDEKTİF\nBÜROSU", justify="left", anchor="w",
            font=tema.font(24, kalin=True), text_color=tema.RENKLER["metin"],
        ).grid(row=1, column=0, sticky="w", padx=22, pady=(26, 0))
        ctk.CTkLabel(
            cubuk, text="Vaka Yönetim Sistemi", anchor="w",
            font=tema.font(12), text_color=tema.RENKLER["soluk_metin"],
        ).grid(row=2, column=0, sticky="w", padx=22, pady=(2, 28))

        for sira, (anahtar, ad, _) in enumerate(SAYFA_TANIMLARI, start=3):
            buton = ctk.CTkButton(
                cubuk, text=ad, anchor="w", height=40, corner_radius=8,
                font=tema.font(14), fg_color="transparent",
                hover_color=tema.RENKLER["secili"], text_color=tema.RENKLER["metin"],
                command=lambda a=anahtar: self.sayfa_goster(a),
            )
            buton.grid(row=sira, column=0, sticky="ew", padx=12, pady=2)
            self.menu_butonlari[anahtar] = buton

        cubuk.grid_rowconfigure(len(SAYFA_TANIMLARI) + 3, weight=1)
        ctk.CTkLabel(
            cubuk, text="MBP 207 · S2 · G12", font=tema.font(11),
            text_color=tema.RENKLER["soluk_metin"],
        ).grid(row=len(SAYFA_TANIMLARI) + 4, column=0, sticky="w", padx=22, pady=18)

    def _sayfa_olustur(self, anahtar):
        if anahtar == "ana_panel":
            return AnaPanel(self.icerik, self.vt)
        ad, sorumlu = next((a, s) for k, a, s in SAYFA_TANIMLARI if k == anahtar)
        return YapimAsamasinda(self.icerik, ad, sorumlu)

    def sayfa_goster(self, anahtar):
        if anahtar not in self.sayfalar:
            sayfa = self._sayfa_olustur(anahtar)
            sayfa.grid(row=0, column=0, sticky="nsew")
            self.sayfalar[anahtar] = sayfa
        self.sayfalar[anahtar].tkraise()

        for a, buton in self.menu_butonlari.items():
            secili = a == anahtar
            buton.configure(
                fg_color=tema.RENKLER["secili"] if secili else "transparent",
                font=tema.font(14, kalin=secili),
            )


class AnaPanel(ctk.CTkFrame):
    """Vaka listesi ve duruma göre vaka sayıları."""

    DURUMLAR = ("Açık", "Soruşturmada", "Çözüldü", "Kapandı")

    def __init__(self, master, vt):
        super().__init__(master, fg_color=tema.RENKLER["arka_plan"])
        self.vt = vt
        self.sayi_etiketleri = {}

        for sutun in range(4):
            self.grid_columnconfigure(sutun, weight=1, uniform="kart")
        self.grid_rowconfigure(2, weight=1)

        self._baslik_olustur()
        self._kartlari_olustur()
        self._tabloyu_olustur()
        self.yenile()

    def _baslik_olustur(self):
        ust = ctk.CTkFrame(self, fg_color="transparent")
        ust.grid(row=0, column=0, columnspan=4, sticky="ew", pady=(0, 18))
        ust.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            ust, text="Ana Panel", anchor="w", font=tema.font(26, kalin=True),
            text_color=tema.RENKLER["metin"],
        ).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(
            ust, text="Büronun vakalarına genel bakış", anchor="w", font=tema.font(13),
            text_color=tema.RENKLER["soluk_metin"],
        ).grid(row=1, column=0, sticky="w")
        ctk.CTkButton(
            ust, text="Yenile", width=100, height=36, font=tema.font(13),
            fg_color=tema.RENKLER["vurgu"], hover_color=tema.RENKLER["vurgu_hover"],
            command=self.yenile,
        ).grid(row=0, column=1, rowspan=2, sticky="e")

    def _kartlari_olustur(self):
        for sutun, durum in enumerate(self.DURUMLAR):
            kart = ctk.CTkFrame(
                self, corner_radius=12, fg_color=tema.RENKLER["kart"],
                border_width=1, border_color=tema.RENKLER["kart_kenar"],
            )
            kart.grid(row=1, column=sutun, sticky="ew", padx=(0 if sutun == 0 else 8, 0), pady=(0, 18))
            kart.grid_columnconfigure(1, weight=1)

            ctk.CTkFrame(kart, width=4, height=56, corner_radius=2,
                         fg_color=tema.DURUM_RENKLERI[durum]).grid(row=0, column=0, rowspan=2, padx=(14, 12), pady=16)
            sayi = ctk.CTkLabel(kart, text="–", anchor="w", font=tema.font(28, kalin=True),
                                text_color=tema.RENKLER["metin"])
            sayi.grid(row=0, column=1, sticky="sw", pady=(12, 0))
            ctk.CTkLabel(kart, text=durum, anchor="w", font=tema.font(12),
                         text_color=tema.RENKLER["soluk_metin"]).grid(row=1, column=1, sticky="nw", pady=(0, 12))
            self.sayi_etiketleri[durum] = sayi

    def _tabloyu_olustur(self):
        kutu = ctk.CTkFrame(
            self, corner_radius=12, fg_color=tema.RENKLER["kart"],
            border_width=1, border_color=tema.RENKLER["kart_kenar"],
        )
        kutu.grid(row=2, column=0, columnspan=4, sticky="nsew")
        kutu.grid_columnconfigure(0, weight=1)
        kutu.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(kutu, text="Vakalar", anchor="w", font=tema.font(16, kalin=True),
                     text_color=tema.RENKLER["metin"]).grid(row=0, column=0, sticky="w", padx=18, pady=(14, 8))

        stil = tema.tablo_stili_uygula(self)
        sutunlar = ("no", "baslik", "durum", "tarih", "dedektif")
        self.tablo = ttk.Treeview(kutu, columns=sutunlar, show="headings", style=stil, selectmode="browse")
        for sutun, baslik, genislik, yayil in (
            ("no", "NO", 60, False),
            ("baslik", "BAŞLIK", 320, True),
            ("durum", "DURUM", 150, False),
            ("tarih", "OLAY TARİHİ", 160, False),
            ("dedektif", "DEDEKTİF", 180, False),
        ):
            self.tablo.heading(sutun, text=baslik, anchor="w")
            self.tablo.column(sutun, width=genislik, stretch=yayil, anchor="w")
        self.tablo.tag_configure("tek", background=tema.RENKLER["kart"])
        self.tablo.tag_configure("cift", background="#262a33")
        self.tablo.grid(row=1, column=0, sticky="nsew", padx=(14, 0), pady=(0, 14))

        kaydirma = ctk.CTkScrollbar(kutu, command=self.tablo.yview)
        kaydirma.grid(row=1, column=1, sticky="ns", padx=(2, 8), pady=(0, 14))
        self.tablo.configure(yscrollcommand=kaydirma.set)

        self.bos_mesaj = ctk.CTkLabel(kutu, text="", font=tema.font(13),
                                      text_color=tema.RENKLER["soluk_metin"], fg_color=tema.RENKLER["kart"])

    def yenile(self):
        self.tablo.delete(*self.tablo.get_children())

        if self.vt is None:
            self._sayilari_goster(None)
            self._bos_mesaj_goster("Veri tabanı bağlantısı henüz yok.\n"
                                   "VeriTabani sınıfı yazılınca vakalar burada listelenecek.")
            return

        try:
            vakalar = self.vt.vakalari_listele()
        except Exception as hata:
            messagebox.showerror("Veri tabanı hatası", f"Vakalar okunamadı:\n{hata}")
            return

        sayilar = {durum: 0 for durum in self.DURUMLAR}
        for sira, (vaka_id, baslik, durum, tarih, dedektif) in enumerate(vakalar):
            self.tablo.insert("", "end", iid=str(vaka_id), tags=("cift" if sira % 2 else "tek",),
                              values=(vaka_id, baslik, f"●  {durum}", tarih, dedektif))
            if durum in sayilar:
                sayilar[durum] += 1
        self._sayilari_goster(sayilar)

        if vakalar:
            self.bos_mesaj.place_forget()
        else:
            self._bos_mesaj_goster("Henüz kayıtlı vaka yok.")

    def _sayilari_goster(self, sayilar):
        for durum, etiket in self.sayi_etiketleri.items():
            etiket.configure(text="–" if sayilar is None else str(sayilar[durum]))

    def _bos_mesaj_goster(self, metin):
        self.bos_mesaj.configure(text=metin)
        self.bos_mesaj.place(relx=0.5, rely=0.5, anchor="center")


class YapimAsamasinda(ctk.CTkFrame):
    """Henüz yazılmamış ekranlar için geçici sayfa."""

    def __init__(self, master, baslik, sorumlu):
        super().__init__(master, fg_color=tema.RENKLER["arka_plan"])
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self, text=baslik, anchor="w", font=tema.font(26, kalin=True),
                     text_color=tema.RENKLER["metin"]).grid(row=0, column=0, sticky="w")

        kutu = ctk.CTkFrame(self, corner_radius=12, fg_color=tema.RENKLER["kart"],
                            border_width=1, border_color=tema.RENKLER["kart_kenar"])
        kutu.grid(row=1, column=0, sticky="nsew", pady=(18, 0))
        ctk.CTkLabel(
            kutu, text=f"Bu ekran yapım aşamasında.\nSorumlu: {sorumlu}",
            font=tema.font(14), text_color=tema.RENKLER["soluk_metin"],
        ).place(relx=0.5, rely=0.5, anchor="center")
