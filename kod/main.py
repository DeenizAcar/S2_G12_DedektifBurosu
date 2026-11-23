"""DedektifBurosu — uygulamanın başlangıç noktası."""
from pathlib import Path
from tkinter import messagebox

from gui.ana_pencere import AnaPencere
from veritabani import VeriTabani

# .db dosyası main.py ile aynı klasörde (kod/) tutulur; teslim zip'inde de burada olur.
DB_YOLU = Path(__file__).resolve().parent / "dedektif_burosu.db"


def main():
    try:
        vt = VeriTabani(DB_YOLU)
    except Exception as hata:
        # Veri tabanı açılamazsa uygulama yine açılır, "bağlantısız" modda çalışır.
        messagebox.showerror("Veri tabanı hatası", f"Veri tabanı açılamadı:\n{hata}")
        vt = None

    uygulama = AnaPencere(vt)
    uygulama.mainloop()

    if vt is not None:
        vt.kapat()


if __name__ == "__main__":
    main()
