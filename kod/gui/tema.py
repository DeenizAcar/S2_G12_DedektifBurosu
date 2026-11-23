"""Uygulamanın ortak renkleri, yazı tipleri ve tablo stili.

Tüm ekranlar renkleri buradan alır; böylece tema tek yerden değiştirilir.
"""
from tkinter import ttk

import customtkinter as ctk

YAZI_TIPI = "Segoe UI"

RENKLER = {
    "arka_plan": "#14161a",
    "kenar_cubugu": "#1b1e24",
    "kart": "#22262e",
    "kart_kenar": "#2e333d",
    "vurgu": "#d64545",        # "kırmızı ip" rengi
    "vurgu_hover": "#b83a3a",
    "metin": "#e8e6e3",
    "soluk_metin": "#9aa0a8",
    "secili": "#2b303a",
}

DURUM_RENKLERI = {
    "Açık": "#e0b44c",
    "Soruşturmada": "#4a90d9",
    "Çözüldü": "#4caf7a",
    "Kapandı": "#7d838c",
}


def font(boyut, kalin=False):
    return ctk.CTkFont(family=YAZI_TIPI, size=boyut, weight="bold" if kalin else "normal")


def tablo_stili_uygula(widget, stil_adi="Koyu.Treeview"):
    """ttk.Treeview'i koyu temaya uydurur. Stil adını döndürür."""
    stil = ttk.Style(widget)
    stil.theme_use("clam")
    stil.configure(
        stil_adi,
        background=RENKLER["kart"],
        fieldbackground=RENKLER["kart"],
        foreground=RENKLER["metin"],
        rowheight=34,
        borderwidth=0,
        font=(YAZI_TIPI, 11),
    )
    stil.map(
        stil_adi,
        background=[("selected", RENKLER["vurgu"])],
        foreground=[("selected", "#ffffff")],
    )
    stil.configure(
        f"{stil_adi}.Heading",
        background=RENKLER["kenar_cubugu"],
        foreground=RENKLER["soluk_metin"],
        relief="flat",
        font=(YAZI_TIPI, 10, "bold"),
        padding=(8, 6),
    )
    stil.map(f"{stil_adi}.Heading", background=[("active", RENKLER["secili"])])
    stil.layout(stil_adi, [("Treeview.treearea", {"sticky": "nswe"})])
    return stil_adi
