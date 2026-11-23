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
        self._ad = deger.strip()

    @property
    def soyad(self):
        return self._soyad

    @soyad.setter
    def soyad(self, deger):
        if deger.strip() == "":
            raise ValueError("Soyad Boş Olamaz")
        self._soyad = deger.strip()


    def __str__(self):
        return f"Ad: {self.ad} Soyad: {self.soyad}"


class Supheli(Kisi):
    def __init__(self, ad, soyad, tc=None, d_tarihi=None, telefon=None, adres=None, id=None, motif=None):
        super().__init__(ad, soyad, tc, d_tarihi, telefon, adres, id)
        self.motif = motif

    @property
    def motif(self):
        return self._motif

    @motif.setter
    def motif(self, deger):
        if deger is None:
            self._motif = deger
        else:
            self._motif = deger.strip()
            if deger.strip() == "":
                self._motif = None

    def motifi_var_mi(self):
        if self.motif is not None:
            return True
        else:
            return False

    def __str__(self):
        return f"Şüpheli: {super().__str__()}"


class Tanik(Kisi):
    def __init__(self, ad, soyad, tc=None, d_tarihi=None, telefon=None, adres=None, id=None, guvenilirlik=50):
        super().__init__(ad, soyad, tc, d_tarihi, telefon, adres, id)
        self.guvenilirlik = guvenilirlik

    @property
    def guvenilirlik(self):
        return self._guvenilirlik

    @guvenilirlik.setter
    def guvenilirlik(self, deger):
        if not isinstance(deger, int):
            raise ValueError("Guvenilirlik Tam Sayı Olmalıdır")
        if not 0 <= deger <= 100:
            raise ValueError("Güvenilirlik 0 İle 100 Arasında Olmalıdır")
        self._guvenilirlik = deger

    def guvenilir_mi(self):
        if self.guvenilirlik >= 60:
            return True
        else:
            return False

    def __str__(self):
        return f"Tanık: {super().__str__()}"