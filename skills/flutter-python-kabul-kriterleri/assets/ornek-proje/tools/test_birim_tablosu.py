import json

import pytest

from birim_tablosu import main, oku


def test_f4_satir_sayisi_csv_ile_ayni(tmp_path):
    cikti = tmp_path / "birimler.json"
    assert main(["", "data/birimler.csv", str(cikti)]) == 0
    assert len(json.loads(cikti.read_text(encoding="utf-8"))) == 3


def test_f4_yanlis_baslik_reddedilir(tmp_path):
    csv_yolu = tmp_path / "x.csv"
    csv_yolu.write_text("a,b\n1,2\n", encoding="utf-8")
    with pytest.raises(ValueError):
        oku(csv_yolu)
