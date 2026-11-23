"""Masa, kâğıt, kraft dosya ve damga görüntülerini Pillow ile kodla üretir.

Hiçbir hazır görsel dosyası kullanılmaz; dokular gürültüden (noise)
renklendirilerek oluşturulur. Aynı boyuttaki dokular önbellekte tutulur.
"""
from functools import lru_cache

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageOps

KAGIT_TONLARI = {
    "krem": ((214, 204, 176), (242, 235, 214), 14),
    "beyaz": ((222, 220, 212), (250, 249, 244), 10),
    "kraft": ((172, 136, 82), (212, 178, 120), 16),
    "mantar": ((120, 82, 48), (200, 152, 98), 34),
}


def _vinyet(w, h, guc):
    """Kenarlara doğru koyulaşan maske (0-255)."""
    kucuk = Image.new("L", (64, 64), 0)
    ImageDraw.Draw(kucuk).ellipse((-10, -10, 74, 74), fill=255)
    maske = kucuk.filter(ImageFilter.GaussianBlur(10)).resize((w, h), Image.BICUBIC)
    return maske.point(lambda v: int(255 - guc + v * guc / 255))


def _carp(img, maske):
    return ImageChops.multiply(img, Image.merge("RGB", (maske, maske, maske)))


@lru_cache(maxsize=8)
def masa(w, h):
    """Zeytin yeşili, hafif çizikli metal masa yüzeyi."""
    w, h = max(1, w), max(1, h)
    koyu, acik = (40, 46, 38), (84, 92, 77)
    taban = ImageOps.colorize(Image.effect_noise((w, h), 22).filter(ImageFilter.GaussianBlur(0.6)), koyu, acik)
    cizgiler = ImageOps.colorize(Image.effect_noise((8, h), 40).resize((w, h), Image.BILINEAR), koyu, acik)
    img = Image.blend(taban, cizgiler, 0.25)
    return _carp(img, _vinyet(w, h, 120))


@lru_cache(maxsize=64)
def kagit(w, h, ton="krem"):
    """Kâğıt, kraft veya mantar dokusu (RGB)."""
    w, h = max(1, w), max(1, h)
    koyu, acik, sigma = KAGIT_TONLARI[ton]
    gurultu = Image.effect_noise((w, h), sigma)
    if ton == "mantar":
        gurultu = gurultu.filter(ImageFilter.GaussianBlur(0.7))
    img = ImageOps.colorize(gurultu, koyu, acik)
    return _carp(img, _vinyet(w, h, 40))


def yazi_tipi(boyut, kalin=False):
    adaylar = ("courbd.ttf", "DejaVuSansMono-Bold.ttf") if kalin else ("cour.ttf", "DejaVuSansMono.ttf")
    for ad in adaylar:
        try:
            return ImageFont.truetype(ad, max(6, int(boyut)))
        except OSError:
            continue
    return ImageFont.load_default()


def metni_sigdir(metin, font, genislik):
    """Metin genişliğe sığmıyorsa sonunu '…' ile keser."""
    if font.getlength(metin) <= genislik:
        return metin
    while metin and font.getlength(metin + "…") > genislik:
        metin = metin[:-1]
    return metin.rstrip() + "…"


@lru_cache(maxsize=64)
def damga(metin, renk, boyut, aci=-12):
    """Çerçeveli, mürekkebi yer yer eksik, eğik bir damga (RGBA)."""
    font = yazi_tipi(boyut, kalin=True)
    sol, ust, sag, alt = ImageDraw.Draw(Image.new("L", (1, 1))).textbbox((0, 0), metin, font=font)
    kalinlik = max(2, boyut // 9)
    bosluk = max(4, boyut // 2)
    w = (sag - sol) + 2 * (bosluk + kalinlik)
    h = (alt - ust) + 2 * (bosluk + kalinlik)

    maske = Image.new("L", (w, h), 0)
    cizim = ImageDraw.Draw(maske)
    yarim = kalinlik // 2
    cizim.rounded_rectangle((yarim, yarim, w - 1 - yarim, h - 1 - yarim),
                            radius=max(2, boyut // 4), outline=255, width=kalinlik)
    cizim.text((bosluk + kalinlik - sol, bosluk + kalinlik - ust), metin, font=font, fill=255)

    delikler = Image.effect_noise((w, h), 70).point(lambda v: 0 if v < 62 else 255)
    maske = ImageChops.multiply(maske, delikler).point(lambda v: v * 220 // 255)

    img = Image.new("RGBA", (w, h), tuple(renk) + (0,))
    img.putalpha(maske)
    return img.rotate(aci, resample=Image.BICUBIC, expand=True)


def golge(img, bulaniklik=8, opaklik=0.45):
    """Bir RGBA görüntünün yumuşak gölgesi. (gölge, kenar_payı) döndürür."""
    pay = bulaniklik * 2
    alfa = Image.new("L", (img.width + 2 * pay, img.height + 2 * pay), 0)
    alfa.paste(img.getchannel("A"), (pay, pay))
    alfa = alfa.filter(ImageFilter.GaussianBlur(bulaniklik)).point(lambda v: int(v * opaklik))
    sonuc = Image.new("RGBA", alfa.size, (0, 0, 0, 0))
    sonuc.putalpha(alfa)
    return sonuc, pay


def _yuvarlak_maske(w, h, yaricap):
    maske = Image.new("L", (w, h), 0)
    ImageDraw.Draw(maske).rounded_rectangle((0, 0, w - 1, h - 1), radius=yaricap, fill=255)
    return maske


def klasor(w, h, vaka_no, baslik, tarih, durum, durum_renk, aci):
    """Üzerinde vaka etiketi ve durum damgası olan kraft dosya (RGBA)."""
    sekme_h = max(8, int(h * 0.17))
    img = Image.new("RGBA", (w, h + sekme_h), (0, 0, 0, 0))

    # dosyanın arkasından taşan evrak
    evrak = kagit(int(w * 0.42), int(h * 0.5), "krem")
    img.paste(evrak, (int(w * 0.52), int(sekme_h * 0.3)))

    # sekme ve gövde
    sekme_w = int(w * 0.34)
    img.paste(kagit(sekme_w, sekme_h + 10, "kraft"), (int(w * 0.04), 0), _yuvarlak_maske(sekme_w, sekme_h + 10, 8))
    img.paste(kagit(w, h, "kraft"), (0, sekme_h))

    cizim = ImageDraw.Draw(img)
    cizim.rectangle((0, sekme_h, w - 1, h + sekme_h - 1), outline=(132, 100, 56), width=2)
    cizim.text((int(w * 0.07), int(sekme_h * 0.15)), f"VAKA {vaka_no:04d}",
               font=yazi_tipi(h * 0.11, kalin=True), fill=(70, 52, 28))

    # beyaz etiket
    x1, y1 = int(w * 0.05), sekme_h + int(h * 0.16)
    x2, y2 = int(w * 0.64), sekme_h + int(h * 0.66)
    img.paste(kagit(x2 - x1, y2 - y1, "beyaz"), (x1, y1))
    cizim.rectangle((x1, y1, x2, y2), outline=(120, 110, 90), width=1)
    baslik_font = yazi_tipi(h * 0.13, kalin=True)
    cizim.text((x1 + 8, y1 + 6), metni_sigdir(baslik, baslik_font, x2 - x1 - 16),
               font=baslik_font, fill=(35, 35, 35))
    cizim.text((x1 + 8, y1 + 8 + int(h * 0.17)), f"OLAY: {tarih}",
               font=yazi_tipi(h * 0.095), fill=(85, 85, 85))

    # durum damgası
    dmg = damga(durum.upper(), durum_renk, max(8, int(h * 0.12)), 9)
    dx = max(x2 + 4, w - dmg.width - 8)
    dy = sekme_h + max(2, (h - dmg.height) // 2)
    if dx + dmg.width <= w and dy + dmg.height <= h + sekme_h:
        img.alpha_composite(dmg, (dx, dy))

    return img.rotate(aci, resample=Image.BICUBIC, expand=True)


@lru_cache(maxsize=16)
def siluet(w, h, zemin=(66, 70, 64), renk=(140, 144, 134)):
    """Fotoğrafı olmayan kişi için baş-omuz silüeti (RGB)."""
    w, h = max(4, w), max(4, h)
    img = Image.new("RGB", (w, h), zemin)
    cizim = ImageDraw.Draw(img)
    r = w * 0.17
    orta = w / 2
    cizim.ellipse((orta - r, h * 0.2, orta + r, h * 0.2 + 2 * r), fill=renk)
    cizim.ellipse((orta - 2.5 * r, h * 0.24 + 2 * r, orta + 2.5 * r, h * 1.25), fill=renk)
    return img


def kimlik_karti(w, h):
    """Giriş ekranındaki boş personel kartı (RGBA)."""
    img = kagit(w, h, "krem").convert("RGBA")
    cizim = ImageDraw.Draw(img)
    serit_h = int(h * 0.14)
    cizim.rectangle((0, 0, w, serit_h), fill=(52, 74, 60))
    cizim.text((22, serit_h // 2), "PERSONEL GİRİŞ KARTI", anchor="lm",
               font=yazi_tipi(serit_h * 0.42, kalin=True), fill=(236, 227, 200))
    cizim.text((w - 22, serit_h // 2), "No. 207-G12", anchor="rm",
               font=yazi_tipi(serit_h * 0.3), fill=(200, 192, 166))

    # fotoğraf alanı ve silüet
    fx1, fy1, fx2, fy2 = 24, serit_h + 22, 24 + int(w * 0.25), serit_h + 22 + int(h * 0.5)
    img.paste(siluet(fx2 - fx1, fy2 - fy1), (fx1, fy1))
    cizim.rectangle((fx1, fy1, fx2, fy2), outline=(40, 40, 40), width=2)
    cizim.text(((fx1 + fx2) // 2, fy2 + 14), "FOTOĞRAF", anchor="mm", font=yazi_tipi(11), fill=(110, 104, 90))

    # sabit form yazıları
    sol = fx2 + 28
    kucuk = yazi_tipi(13, kalin=True)
    cizim.text((sol, serit_h + 26), "AD SOYAD:", font=kucuk, fill=(60, 56, 48))
    cizim.line((sol, serit_h + 66, w - 26, serit_h + 66), fill=(150, 140, 115), width=1)
    cizim.text((sol, serit_h + 84), "SİCİL NO:", font=kucuk, fill=(60, 56, 48))
    cizim.text((22, h - 18), "Kart sahibi dışında kullanılamaz. Kaybı hâlinde büroya bildiriniz.",
               anchor="lm", font=yazi_tipi(10), fill=(120, 112, 96))
    cizim.rectangle((0, 0, w - 1, h - 1), outline=(150, 138, 108), width=2)
    return img
