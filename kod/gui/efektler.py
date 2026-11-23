"""Ses ve animasyon efektleri: damga basma, daktilo yazısı, titreme.

Animasyonlar Tkinter'ın after() zamanlayıcısıyla kare kare çalışır.
Ekran bu sırada kapanırsa animasyon sessizce durur.
"""
import tkinter as tk
from pathlib import Path

from PIL import ImageTk

from gui import dokular, tema

try:
    import winsound
except ImportError:   # Windows dışında ses çalınmaz, uygulama yine çalışır
    winsound = None

SES_KLASORU = Path(__file__).parent / "sesler"


class Ses:
    """Kısa .wav efektlerini çalar; kapatılabilir."""

    def __init__(self):
        self.acik = True

    def cal(self, ad):
        if not self.acik or winsound is None:
            return
        yol = SES_KLASORU / f"{ad}.wav"
        if not yol.exists():
            return
        try:
            winsound.PlaySound(str(yol), winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT)
        except RuntimeError:
            pass


def _resim_sakla(canvas, resimler):
    """PhotoImage'lar Python tarafında tutulmazsa silinir; canvas'a bağlarız."""
    if not hasattr(canvas, "efekt_resimleri"):
        canvas.efekt_resimleri = []
    canvas.efekt_resimleri.extend(resimler)


def damga_bas(canvas, x, y, metin, renk, boyut, aci=-12, ses=None, bitince=None, tags=()):
    """Büyükten küçülerek kâğıda inen bir damga. Canvas öğe kimliğini döndürür."""
    temel = dokular.damga(metin, tema.rgb(renk), boyut, aci)
    olcekler = (2.1, 1.65, 1.3, 1.08, 0.97, 1.0)
    kareler = []
    for olcek in olcekler:
        kare = temel.resize((max(1, int(temel.width * olcek)), max(1, int(temel.height * olcek))))
        if olcek > 1:
            oran = min(1.0, 0.2 + 0.8 / olcek)
            kare.putalpha(kare.getchannel("A").point(lambda v, o=oran: int(v * o)))
        kareler.append(ImageTk.PhotoImage(kare))
    _resim_sakla(canvas, kareler)

    oge = canvas.create_image(x, y, image=kareler[0], tags=tags)

    def adim(i):
        try:
            if not canvas.winfo_exists():
                return
            canvas.itemconfigure(oge, image=kareler[i])
            if i == len(kareler) - 2 and ses:
                ses.cal("damga")
            if i < len(kareler) - 1:
                canvas.after(30, adim, i + 1)
            elif bitince:
                bitince(oge)
        except tk.TclError:
            pass

    canvas.after(10, adim, 0)
    return oge


def daktilo_yaz(canvas, oge, metin, hiz=38, ses=None, bitince=None):
    """Canvas üzerindeki bir metni harf harf yazar."""

    def adim(i):
        try:
            if not canvas.winfo_exists():
                return
            canvas.itemconfigure(oge, text=metin[:i] + ("▌" if i < len(metin) else ""))
            if ses and i > 0 and not metin[i - 1].isspace() and i % 2 == 0:
                ses.cal("daktilo")
            if i < len(metin):
                bekle = hiz * 6 if metin[i - 1:i] == "\n" else hiz
                canvas.after(bekle, adim, i + 1)
            else:
                if ses:
                    ses.cal("zil")
                if bitince:
                    bitince()
        except tk.TclError:
            pass

    adim(0)


def titret(canvas, tag, genlik=10):
    """Bir öğe grubunu sağa sola sallar (hatalı giriş için)."""
    konumlar = [0, genlik, -genlik, genlik * 0.6, -genlik * 0.6, genlik * 0.3, -genlik * 0.3, 0]

    def adim(i):
        try:
            if not canvas.winfo_exists() or i >= len(konumlar):
                return
            canvas.move(tag, konumlar[i] - konumlar[i - 1], 0)
            canvas.after(35, adim, i + 1)
        except tk.TclError:
            pass

    adim(1)
