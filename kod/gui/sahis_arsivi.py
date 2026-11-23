"""Şahıs Arşivi: kişilerin listelendiği, eklendiği, güncellendiği ve silindiği ekran.

Sol tarafta kayıt listesi, sağda seçili kişinin "şahıs kartı" durur.
Doğrulama kuralları Kisi sınıfındadır; bu ekran yalnızca hataları yakalayıp gösterir.

Kullanılan VeriTabani metotları:
  kisileri_listele()  -> [(id, ad, soyad, tc_no, dogum_tarihi, telefon, adres), ...]
  kisi_ekle(kisi)     -> yeni id
  kisi_guncelle(kisi)
  kisi_sil(kisi_id)
"""
import tkinter as tk
from tkinter import messagebox, ttk

import customtkinter as ctk

from gui import efektler, tema
from gui.sahne import Sahne
from modeller.kisi import Kisi

# (alan anahtarı, kartta görünen etiket, örnek)
ALANLAR = (
    ("ad", "AD", "Can"),
    ("soyad", "SOYAD", "Yıldız"),
    ("tc", "TC KİMLİK NO", "11 haneli"),
    ("dogum_tarihi", "DOĞUM TARİHİ", "YYYY-AA-GG"),
    ("telefon", "TELEFON", "0555 000 00 00"),
    ("adres", "ADRES", "Semt, ilçe"),
)


class SahisArsivi(Sahne):
    def __init__(self, master, uygulama, vaka_id=None):
        super().__init__(master, uygulama)
        self.kayitlar = {}          # id -> veri tabanı satırı
        self.secili_id = None
        self.durum_metni = ""
        self.durum_rengi = tema.RENKLER["kirmizi"]
        self.liste_notu = ""

        self._widgetlari_olustur()
        self.listeyi_yenile()

    # --- widget'lar (bir kez oluşturulur, her çizimde yeniden yerleştirilir) ----
    def _widgetlari_olustur(self):
        kagit = "#f3eee2"
        girdi = dict(corner_radius=3, border_width=2, fg_color="#fbf8ef", border_color="#9a8f72",
                     bg_color=kagit, text_color=tema.RENKLER["murekkep"],
                     placeholder_text_color="#b0a78f", font=(tema.DAKTILO, 15, "bold"))

        self.arama = ctk.CTkEntry(self.canvas, placeholder_text="ad, soyad veya TC ile ara", **girdi)
        self.arama.bind("<KeyRelease>", lambda _: self._listeyi_doldur())

        self.girdiler = {}
        for anahtar, _, ornek in ALANLAR:
            alan = ctk.CTkEntry(self.canvas, placeholder_text=ornek, **girdi)
            alan.bind("<Return>", lambda _: self.kaydet())
            self.girdiler[anahtar] = alan

        dugme = dict(corner_radius=3, height=44, font=(tema.DAKTILO, 15, "bold"),
                     text_color="#f5eedb", bg_color=tema.RENKLER["masa"])
        self.yeni_dugmesi = ctk.CTkButton(self.canvas, text="+ YENİ KART", fg_color="#5d6458",
                                          hover_color="#4a5046", command=self.yeni_kart, **dugme)
        self.kaydet_dugmesi = ctk.CTkButton(self.canvas, text="KAYDET", fg_color=tema.RENKLER["yesil"],
                                            hover_color="#25552e", command=self.kaydet, **dugme)
        self.sil_dugmesi = ctk.CTkButton(self.canvas, text="SİL", fg_color=tema.RENKLER["kirmizi"],
                                         hover_color=tema.RENKLER["kirmizi_hover"], command=self.sil, **dugme)

        self.liste_cercevesi = tk.Frame(self.canvas, bg=kagit, highlightthickness=0)
        stil = tema.tablo_stili_uygula(self)
        self.liste = ttk.Treeview(self.liste_cercevesi, columns=("no", "ad", "tc", "telefon"),
                                  show="headings", style=stil, selectmode="browse")
        for sutun, baslik, genislik, yayil in (("no", "NO", 60, False), ("ad", "AD SOYAD", 220, True),
                                                ("tc", "TC KİMLİK NO", 150, False),
                                                ("telefon", "TELEFON", 150, False)):
            self.liste.heading(sutun, text=baslik, anchor="w")
            self.liste.column(sutun, width=genislik, stretch=yayil, anchor="w")
        self.liste.tag_configure("cift", background="#e4dcc4")
        kaydirma = ctk.CTkScrollbar(self.liste_cercevesi, command=self.liste.yview,
                                    button_color="#b3a888", button_hover_color="#9a8f72", fg_color=kagit)
        self.liste.configure(yscrollcommand=kaydirma.set)
        self.liste.pack(side="left", fill="both", expand=True)
        kaydirma.pack(side="right", fill="y")
        self.liste.bind("<<TreeviewSelect>>", self._secim_degisti)

    # --- çizim -----------------------------------------------------------------
    def ciz(self):
        c = self.canvas
        self.ust_bant_ciz("ŞAHIS ARŞİVİ")
        self.ust_bant_dugmesi(self.W - 20, "[ ◂ MASAYA DÖN ]", self.uyg.masaya_don)
        murekkep = tema.RENKLER["murekkep"]

        # sol: kayıt listesi
        self.kagit(30, 22, 690, 700, ton="beyaz")
        c.create_text(*self.P(56, 48), anchor="nw", text="ŞAHIS KAYITLARI",
                      font=self.F(17, True), fill=murekkep)
        self.sayi_ogesi = c.create_text(*self.P(664, 52), anchor="ne", text="",
                                        font=self.F(12), fill=tema.RENKLER["soluk_murekkep"])
        c.create_line(*self.K(56, 78, 664, 78), fill=murekkep, width=self.px(2))
        c.create_text(*self.P(56, 106), anchor="w", text="ARA:", font=self.F(12, True), fill=murekkep)
        self.arama.configure(width=self.wpx(548), height=self.wpx(36))
        c.create_window(*self.P(116, 106), window=self.arama, anchor="w")
        c.create_window(*self.P(56, 134), window=self.liste_cercevesi, anchor="nw",
                        width=self.px(608), height=self.px(546))
        self.liste_notu_ogesi = c.create_text(*self.P(360, 400), text=self.liste_notu, width=self.px(520),
                                              font=self.F(13), fill=tema.RENKLER["soluk_murekkep"])
        self._sayiyi_guncelle()

        # sağ: şahıs kartı
        self.kagit(728, 22, 1252, 566, ton="beyaz", tags=("kart",))
        for y in range(126, 560, 31):
            c.create_line(*self.K(728, y, 1252, y), fill="#c9d6e3", tags=("kart",))
        c.create_line(*self.K(728, 86, 1252, 86), fill="#d98c8c", width=self.px(2), tags=("kart",))
        c.create_text(*self.P(752, 54), anchor="w", text="ŞAHIS KARTI", font=self.F(18, True),
                      fill=murekkep, tags=("kart",))
        self.kart_no_ogesi = c.create_text(*self.P(1228, 54), anchor="e", text="", font=self.F(14, True),
                                           fill=tema.RENKLER["kirmizi"], tags=("kart",))

        for sira, (anahtar, etiket, _) in enumerate(ALANLAR):
            y = 104 + sira * 66
            c.create_text(*self.P(752, y), anchor="nw", text=etiket, font=self.F(11, True),
                          fill=tema.RENKLER["soluk_murekkep"], tags=("kart",))
            girdi = self.girdiler[anahtar]
            girdi.configure(width=self.wpx(476), height=self.wpx(34))
            c.create_window(*self.P(752, y + 18), window=girdi, anchor="nw", tags=("kart",))

        self.durum_ogesi = c.create_text(*self.P(752, 508), anchor="nw", width=self.px(300),
                                         text=self.durum_metni, font=self.F(13, True),
                                         fill=self.durum_rengi, tags=("kart",))
        self._kart_numarasini_guncelle()

        # düğmeler
        for sira, dugme in enumerate((self.yeni_dugmesi, self.kaydet_dugmesi, self.sil_dugmesi)):
            dugme.configure(width=self.wpx(166), height=self.wpx(46))
            c.create_window(*self.P(728 + sira * 179, 590), window=dugme, anchor="nw")
        c.create_text(*self.P(990, 668), text="Listeden bir kişi seçin ya da yeni kart açın.",
                      font=self.F(12), fill=tema.RENKLER["soluk_metin"])

    def _sayiyi_guncelle(self):
        if hasattr(self, "sayi_ogesi"):
            self.canvas.itemconfigure(self.sayi_ogesi, text=f"{len(self.kayitlar)} KAYIT")

    def _kart_numarasini_guncelle(self):
        if hasattr(self, "kart_no_ogesi"):
            metin = "YENİ KAYIT" if self.secili_id is None else f"No. {self.secili_id:04d}"
            self.canvas.itemconfigure(self.kart_no_ogesi, text=metin)

    def _durum(self, metin, renk=None):
        self.durum_metni = metin
        self.durum_rengi = renk or tema.RENKLER["kirmizi"]
        if hasattr(self, "durum_ogesi"):
            self.canvas.itemconfigure(self.durum_ogesi, text=metin, fill=self.durum_rengi)

    def _liste_notu(self, metin):
        self.liste_notu = metin
        if hasattr(self, "liste_notu_ogesi"):
            self.canvas.itemconfigure(self.liste_notu_ogesi, text=metin)

    # --- liste -----------------------------------------------------------------
    def listeyi_yenile(self):
        """Kayıtları veri tabanından yeniden okur."""
        self.kayitlar = {}
        vt = self.uyg.vt
        if vt is None:
            self._liste_notu("Veri tabanı bağlı değil.")
        else:
            try:
                self.kayitlar = {satir[0]: satir for satir in vt.kisileri_listele()}
                self._liste_notu("" if self.kayitlar else "Arşivde kayıtlı kişi yok.")
            except AttributeError:
                self._liste_notu("VeriTabani.kisileri_listele() metodu henüz yazılmadı.")
            except Exception as hata:
                messagebox.showerror("Veri tabanı hatası", f"Kişiler okunamadı:\n{hata}")
        self._listeyi_doldur()
        self._sayiyi_guncelle()

    def _listeyi_doldur(self):
        aranan = self.arama.get().strip().lower()
        self.liste.delete(*self.liste.get_children())
        sira = 0
        for kisi_id, ad, soyad, tc_no, _, telefon, _ in self.kayitlar.values():
            metin = f"{ad} {soyad} {tc_no or ''}".lower()
            if aranan and aranan not in metin:
                continue
            self.liste.insert("", "end", iid=str(kisi_id), tags=("cift",) if sira % 2 else (),
                              values=(f"{kisi_id:04d}", f"{ad} {soyad}", tc_no or "—", telefon or "—"))
            sira += 1
        if self.secili_id is not None and self.liste.exists(str(self.secili_id)):
            self.liste.selection_set(str(self.secili_id))
            self.liste.see(str(self.secili_id))

    def _secim_degisti(self, _olay=None):
        secim = self.liste.selection()
        if not secim:
            return
        kisi_id = int(secim[0])
        if kisi_id == self.secili_id:
            return
        self.secili_id = kisi_id
        _, ad, soyad, tc_no, dogum, telefon, adres = self.kayitlar[kisi_id]
        for anahtar, deger in zip(("ad", "soyad", "tc", "dogum_tarihi", "telefon", "adres"),
                                  (ad, soyad, tc_no, dogum, telefon, adres)):
            self._girdiye_yaz(anahtar, deger)
        self._durum("")
        self._kart_numarasini_guncelle()
        self.uyg.ses.cal("kagit")

    def _girdiye_yaz(self, anahtar, deger):
        alan = self.girdiler[anahtar]
        alan.delete(0, "end")
        if deger:
            alan.insert(0, deger)

    # --- işlemler --------------------------------------------------------------
    def yeni_kart(self):
        self.secili_id = None
        self.liste.selection_remove(*self.liste.selection())
        for anahtar in self.girdiler:
            self._girdiye_yaz(anahtar, None)
        self._durum("")
        self._kart_numarasini_guncelle()
        self.girdiler["ad"].focus_set()
        self.uyg.ses.cal("kagit")

    def _formdaki_kisi(self):
        """Formdaki değerlerle bir Kisi nesnesi kurar. Kurallar Kisi sınıfındadır."""
        degerler = {anahtar: (alan.get().strip() or None) for anahtar, alan in self.girdiler.items()}
        return Kisi(degerler["ad"] or "", degerler["soyad"] or "", degerler["tc"],
                    degerler["dogum_tarihi"], degerler["telefon"], degerler["adres"], self.secili_id)

    def kaydet(self):
        if not self._baglanti_var_mi():
            return
        try:
            kisi = self._formdaki_kisi()
        except ValueError as hata:
            self._hata_goster(str(hata))
            return

        yeni_kayit = self.secili_id is None
        try:
            if yeni_kayit:
                yeni_id = self.uyg.vt.kisi_ekle(kisi)
                if isinstance(yeni_id, int):
                    self.secili_id = yeni_id
            else:
                self.uyg.vt.kisi_guncelle(kisi)
        except AttributeError as hata:
            self._hata_goster(f"VeriTabani'nda gerekli metot henüz yok ({hata}).")
            return
        except Exception as hata:
            self._hata_goster(self._vt_hatasini_acikla(hata))
            return

        self.listeyi_yenile()
        self._kart_numarasini_guncelle()
        self._durum("Kayıt eklendi." if yeni_kayit else "Kayıt güncellendi.", tema.RENKLER["yesil"])
        self._damga("KAYDEDİLDİ" if yeni_kayit else "GÜNCELLENDİ", tema.RENKLER["yesil"])

    def sil(self):
        if not self._baglanti_var_mi():
            return
        if self.secili_id is None:
            self._hata_goster("Silmek için önce listeden bir kişi seçin.")
            return
        _, ad, soyad, *_ = self.kayitlar[self.secili_id]
        if not messagebox.askyesno("Kaydı sil", f"{ad} {soyad} arşivden kalıcı olarak silinsin mi?\n"
                                                f"Bu işlem geri alınamaz."):
            return
        try:
            self.uyg.vt.kisi_sil(self.secili_id)
        except AttributeError as hata:
            self._hata_goster(f"VeriTabani'nda gerekli metot henüz yok ({hata}).")
            return
        except Exception as hata:
            self._hata_goster(self._vt_hatasini_acikla(hata))
            return

        self._damga("İPTAL", tema.RENKLER["kirmizi"])
        self.after(900, self._silme_sonrasi)

    def _silme_sonrasi(self):
        self.yeni_kart()
        self.listeyi_yenile()
        self._durum("Kayıt silindi.", tema.RENKLER["kirmizi"])

    # --- yardımcılar -----------------------------------------------------------
    def _baglanti_var_mi(self):
        if self.uyg.vt is None:
            self._hata_goster("Veri tabanı bağlı değil; kayıt yapılamaz.")
            return False
        return True

    @staticmethod
    def _vt_hatasini_acikla(hata):
        metin = str(hata)
        if "UNIQUE" in metin and "tc_no" in metin:
            return "Bu TC kimlik numarası başka bir kişiye kayıtlı."
        if "FOREIGN KEY" in metin:
            return "Bu kişi bir vakada fail olarak kayıtlı; önce vakadan çıkarılmalı."
        if "CHECK" in metin:
            return "Bilgilerden biri veri tabanı kurallarına uymuyor."
        return f"Veri tabanı hatası: {metin}"

    def _hata_goster(self, metin):
        self._durum(metin)
        efektler.titret(self.canvas, "kart")

    def _damga(self, metin, renk):
        # giriş kutuları canvas'ın üstünde durduğu için damga kartın boş alt köşesine basılır
        x, y = self.P(1140, 528)
        efektler.damga_bas(self.canvas, x, y, metin, renk, self.px(22), aci=-10, ses=self.uyg.ses,
                           tags=("kart",),
                           bitince=lambda oge: self.after(1100, lambda: self.canvas.delete(oge)))
