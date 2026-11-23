"""DedektifBurosu — uygulamanın başlangıç noktası."""
from gui.ana_pencere import AnaPencere


def main():
    # VeriTabani sınıfı yazılınca burada oluşturulup pencereye verilecek:
    #   vt = VeriTabani("dedektif_burosu.db")
    vt = None
    uygulama = AnaPencere(vt)
    uygulama.mainloop()


if __name__ == "__main__":
    main()
