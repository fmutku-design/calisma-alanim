"""data/birimler.csv → assets/birimler.json (uygulamanın okuduğu offline tablo)."""

import csv
import json
import sys
from pathlib import Path

ALANLAR = ("kategori", "kaynak", "hedef", "carpan")


def oku(yol: Path) -> list[dict]:
    with yol.open(encoding="utf-8", newline="") as f:
        okuyucu = csv.DictReader(f)
        if tuple(okuyucu.fieldnames or ()) != ALANLAR:
            raise ValueError(f"Başlık {ALANLAR} olmalı, {okuyucu.fieldnames} bulundu")
        return [{**s, "carpan": float(s["carpan"])} for s in okuyucu]


def yaz(kayitlar: list[dict], yol: Path) -> None:
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_text(json.dumps(kayitlar, ensure_ascii=False), encoding="utf-8")


def main(argv: list[str]) -> int:
    girdi = Path(argv[1]) if len(argv) > 1 else Path("data/birimler.csv")
    cikti = Path(argv[2]) if len(argv) > 2 else Path("assets/birimler.json")
    yaz(oku(girdi), cikti)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
