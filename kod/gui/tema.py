"""Uygulamanın ortak renkleri ve yazı tipleri.

Görsel dil: Soğuk Savaş dönemi devlet dairesi. Zeytin yeşili metal masa,
krem rengi formlar, kraft dosyalar, mürekkep damgaları ve daktilo yazısı.
Tüm ekranlar renkleri buradan alır; tema tek yerden değiştirilir.
"""
from tkinter import ttk

import customtkinter as ctk

DAKTILO = "Courier New"     # form ve belge yazıları
EL_YAZISI = "Segoe Print"   # not defteri yazıları (yoksa Tk benzerini seçer)
YAZI_TIPI = "Segoe UI"      # sıradan arayüz yazıları

RENKLER = {
    "masa": "#3b4236",
    "masa_golge": "#262b23",
    "ust_bant": "#1d211c",
    "pirinc": "#b08d3c",       # etiket plakaları
    "pirinc_koyu": "#6e5620",
    "kagit": "#ece3c8",
    "kagit_kenar": "#b9ad8c",
    "murekkep": "#2a2a2a",
    "soluk_murekkep": "#6b665a",
    "kirmizi": "#9e2a22",
    "kirmizi_hover": "#7a2019",
    "yesil": "#2f6b3a",
    "mavi_murekkep": "#23407a",
    "metal": "#6a7166",
    "metal_koyu": "#2a2e27",
    "acik_metin": "#e8e0c8",
    "soluk_metin": "#9aa092",
}

# Durum damgalarının mürekkep renkleri
DURUM_RENKLERI = {
    "Açık": "#2c4a7a",
    "Soruşturmada": "#a8322a",
    "Çözüldü": "#2f6b3a",
    "Kapandı": "#4d5156",
}


def rgb(hex_renk):
    """'#rrggbb' -> (r, g, b)"""
    hex_renk = hex_renk.lstrip("#")
    return tuple(int(hex_renk[i:i + 2], 16) for i in (0, 2, 4))


def font(boyut, kalin=False, aile=YAZI_TIPI):
    """CustomTkinter widget'ları için yazı tipi."""
    return ctk.CTkFont(family=aile, size=boyut, weight="bold" if kalin else "normal")


def tablo_stili_uygula(widget, stil_adi="Kagit.Treeview"):
    """ttk.Treeview'i kâğıt temasına uydurur. Stil adını döndürür."""
    stil = ttk.Style(widget)
    stil.theme_use("clam")
    stil.configure(
        stil_adi,
        background=RENKLER["kagit"],
        fieldbackground=RENKLER["kagit"],
        foreground=RENKLER["murekkep"],
        rowheight=32,
        borderwidth=0,
        font=(DAKTILO, 11),
    )
    stil.map(
        stil_adi,
        background=[("selected", RENKLER["kirmizi"])],
        foreground=[("selected", "#ffffff")],
    )
    stil.configure(
        f"{stil_adi}.Heading",
        background="#d6cba8",
        foreground=RENKLER["murekkep"],
        relief="flat",
        font=(DAKTILO, 10, "bold"),
        padding=(8, 6),
    )
    stil.map(f"{stil_adi}.Heading", background=[("active", "#cbbf98")])
    stil.layout(stil_adi, [("Treeview.treearea", {"sticky": "nswe"})])
    return stil_adi
