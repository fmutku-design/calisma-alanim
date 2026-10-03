#!/usr/bin/env python3
"""Kullanıcının tasarım görseli ile uygulamanın ekran görüntüsünü piksel piksel karşılaştırır (T5).

Kullanım:
    python goruntu_karsilastir.py <tasarim.png> <uygulama.png> [--kanal-esigi 16] [--fark-goruntusu fark.png]

Çıktı: farklı piksel yüzdesi. Bir piksel, R/G/B/A kanallarından birindeki fark --kanal-esigi'ni (0–255)
aşarsa farklı sayılır. Boyutlar farklıysa karşılaştırma yapılmaz (çıkış kodu 2) — ölçeklemek tahmin olurdu.
Fark görüntüsü: aynı pikseller soluk gri, farklı pikseller kırmızı.

Sadece Python standart kütüphanesi (zlib, struct) kullanılır. 8-bit, taramasız (non-interlaced)
gri, RGB, gri+alfa ve RGBA PNG'leri okur — Flutter ekran görüntüleri ve Figma dışa aktarımları bu biçimdedir.
"""

from __future__ import annotations

import argparse
import struct
import sys
import zlib
from pathlib import Path

PNG_IMZA = b"\x89PNG\r\n\x1a\n"
KANAL = {0: 1, 2: 3, 4: 2, 6: 4}


def png_oku(yol: Path) -> tuple[int, int, list[bytes]]:
    """(genişlik, yükseklik, satırlar) döndürür; her satır RGBA baytlarıdır."""
    veri = yol.read_bytes()
    if not veri.startswith(PNG_IMZA):
        raise ValueError(f"{yol}: PNG değil")
    i, idat, gen = 8, bytearray(), None
    while i < len(veri):
        uzunluk, tur = struct.unpack(">I4s", veri[i:i + 8])
        govde = veri[i + 8:i + 8 + uzunluk]
        if tur == b"IHDR":
            gen, yuk, derinlik, renk_turu, _, _, tarama = struct.unpack(">IIBBBBB", govde)
            if derinlik != 8 or renk_turu not in KANAL or tarama != 0:
                raise ValueError(f"{yol}: desteklenmeyen PNG (bit derinliği {derinlik}, renk türü {renk_turu}, tarama {tarama})")
        elif tur == b"PLTE":
            raise ValueError(f"{yol}: paletli PNG desteklenmiyor; RGB/RGBA olarak dışa aktar")
        elif tur == b"IDAT":
            idat += govde
        elif tur == b"IEND":
            break
        i += 12 + uzunluk
    if gen is None:
        raise ValueError(f"{yol}: IHDR yok")
    ham = zlib.decompress(bytes(idat))
    bpp = KANAL[renk_turu]
    satir_boyu = gen * bpp
    satirlar, onceki, j = [], bytearray(satir_boyu), 0
    for _ in range(yuk):
        filtre = ham[j]
        satir = bytearray(ham[j + 1:j + 1 + satir_boyu])
        j += 1 + satir_boyu
        for x in range(satir_boyu):
            a = satir[x - bpp] if x >= bpp else 0
            b = onceki[x]
            c = onceki[x - bpp] if x >= bpp else 0
            if filtre == 1:
                satir[x] = (satir[x] + a) & 0xFF
            elif filtre == 2:
                satir[x] = (satir[x] + b) & 0xFF
            elif filtre == 3:
                satir[x] = (satir[x] + ((a + b) >> 1)) & 0xFF
            elif filtre == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                satir[x] = (satir[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 0xFF
        onceki = satir
        satirlar.append(_rgbaya(bytes(satir), renk_turu))
    return gen, yuk, satirlar


def _rgbaya(satir: bytes, renk_turu: int) -> bytes:
    if renk_turu == 6:
        return satir
    cikti = bytearray()
    if renk_turu == 2:
        for k in range(0, len(satir), 3):
            cikti += satir[k:k + 3] + b"\xff"
    elif renk_turu == 0:
        for g in satir:
            cikti += bytes((g, g, g, 255))
    elif renk_turu == 4:
        for k in range(0, len(satir), 2):
            g, al = satir[k], satir[k + 1]
            cikti += bytes((g, g, g, al))
    return bytes(cikti)


def png_yaz(yol: Path, gen: int, yuk: int, satirlar: list[bytes]) -> None:
    ham = b"".join(b"\x00" + s for s in satirlar)

    def parca(tur: bytes, govde: bytes) -> bytes:
        return struct.pack(">I", len(govde)) + tur + govde + struct.pack(">I", zlib.crc32(tur + govde) & 0xFFFFFFFF)

    yol.write_bytes(PNG_IMZA + parca(b"IHDR", struct.pack(">IIBBBBB", gen, yuk, 8, 6, 0, 0, 0))
                    + parca(b"IDAT", zlib.compress(ham, 9)) + parca(b"IEND", b""))


def karsilastir(tasarim: Path, uygulama: Path, kanal_esigi: int, fark_yolu: Path | None) -> tuple[float, str]:
    g1, y1, s1 = png_oku(tasarim)
    g2, y2, s2 = png_oku(uygulama)
    if (g1, y1) != (g2, y2):
        raise ValueError(f"Boyutlar farklı: tasarım {g1}x{y1}, uygulama {g2}x{y2}. "
                         "ekranlar.json → ekran_boyutu × piksel_orani tasarım görseliyle aynı olmalı.")
    farkli, fark_satirlari = 0, []
    for a, b in zip(s1, s2):
        fs = bytearray()
        for k in range(0, len(a), 4):
            if max(abs(a[k] - b[k]), abs(a[k + 1] - b[k + 1]), abs(a[k + 2] - b[k + 2]), abs(a[k + 3] - b[k + 3])) > kanal_esigi:
                farkli += 1
                fs += b"\xff\x00\x00\xff"
            else:
                gri = 200 + (a[k] + a[k + 1] + a[k + 2]) // 3 * 55 // 255
                fs += bytes((gri, gri, gri, 255))
        fark_satirlari.append(bytes(fs))
    if fark_yolu:
        png_yaz(fark_yolu, g1, y1, fark_satirlari)
    toplam = g1 * y1
    yuzde = round(farkli / toplam * 100, 3)
    return yuzde, f"{tasarim.name} ↔ {uygulama.name}: {farkli}/{toplam} piksel farklı (%{yuzde}, kanal eşiği {kanal_esigi}, {g1}x{y1})"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tasarim", type=Path)
    ap.add_argument("uygulama", type=Path)
    ap.add_argument("--kanal-esigi", type=int, default=16)
    ap.add_argument("--fark-goruntusu", type=Path, default=None)
    a = ap.parse_args()
    try:
        _, kanit = karsilastir(a.tasarim, a.uygulama, a.kanal_esigi, a.fark_goruntusu)
    except (ValueError, OSError, zlib.error) as e:
        print(f"ÖLÇÜLEMEDİ: {e}")
        return 2
    print(kanit)
    return 0


if __name__ == "__main__":
    sys.exit(main())
