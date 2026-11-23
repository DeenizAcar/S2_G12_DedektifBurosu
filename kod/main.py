"""DedektifBurosu — uygulamanın başlangıç noktası."""
from gui.ana_pencere import AnaPencere


def main():
    # VeriTabani sınıfı yazılınca burada oluşturulup pencereye verilecek:
    #   vt = VeriTabani("dedektif_burosu.db")
    # Arayüzün şu an VeriTabani'ndan beklediği metotlar:
    #   dedektif_bul(sicil_no)          -> (id, ad, soyad, sicil_no) ya da None
    #   dedektif_vakalari(dedektif_id)  -> [(vaka_id, baslik, durum, olay_baslangic), ...]
    vt = None
    uygulama = AnaPencere(vt)
    uygulama.mainloop()


if __name__ == "__main__":
    main()
