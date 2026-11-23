class Kisi:
    def __init__(self, ad, soyad, tc=None, d_tarihi=None, telefon=None, adres=None, id=None):
        self.ad = ad
        self.soyad = soyad
        self.id = id
        self.telefon = telefon
        self.adres = adres
        self.d_tarihi = d_tarihi
        self.tc = tc

    @property
    def tc(self):
        return self._tc

    @tc.setter
    def tc(self, deger):
        if deger is not None and not (deger.isdigit() and len(deger) == 11):
            raise ValueError("Tc 11 haneli olmalı ve sadece rakam içermeli.")
        self._tc = deger

    @property
    def ad(self):
        return self._ad

    @ad.setter
    def ad(self, deger):
        if deger.strip() == "":
            raise ValueError("Ad Boş Olamaz")
        self._ad = deger

    @property
    def soyad(self):
        return self._soyad

    @soyad.setter
    def soyad(self, deger):
        if deger.strip() == "":
            raise ValueError("Soyad Boş Olamaz")
        self._soyad = deger


    def __str__(self):
        return f"Ad: {self.ad} Soyad: {self.soyad}"


