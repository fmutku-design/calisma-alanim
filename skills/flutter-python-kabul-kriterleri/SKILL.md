---
name: flutter-python-kabul-kriterleri
description: İnternetsiz (offline) çalışan Flutter Android uygulamaları ve onlara eşlik eden Python script/otomasyon/ML işleri için varsayımsız, ölçülebilir ve dürüst çalışma yöntemi. Uygulamanın tasarımını (renk, yazı, boşluk, ekran yerleşimi, ekran görüntüsü), yazılım mimarisini (katmanlar, bağımlılıklar, dosya/fonksiyon uzunluğu), işlevini ve Claude'un kendi davranışını (varsayım, onaysız kod, kanıtsız "bitti" iddiası) script ile sayılan metriklere bağlar. Tasarımı yalnızca kullanıcı verir; Claude tasarım değeri seçmez. Örnek mimari ve adım adım kurulum talimatı içerir. Önce sorar, cevapları eşikli kabul kriterlerine çevirir, onay alınca işi sonuna kadar yapar, ölçer ve GEÇTİ/KALDI/ÖLÇÜLEMEDİ raporuyla teslim eder. Kullanıcı Flutter, Dart, Android, APK, offline/internetsiz uygulama, ekran tasarımı, Figma'dan uygulama, UI, mimari, TFLite/ML modeli, Python ile veri hazırlama, yeni ekran/özellik ekleme, "uygulama yap", "app geliştir", kabul kriteri veya metrik dediğinde mutlaka bu skill'i kullan — "kabul kriteri" kelimesi geçmese bile, Flutter/Android işi istendiği anda kullan.
---

# Flutter + Python (Offline Android) — Tasarımı ve Yazılımı Ölçülebilir Çalışma

## Bu skill neden var

Kullanıcının sorunu: Claude belirsiz bir istek alınca boşlukları kendi tahminiyle dolduruyor — tasarımı kafasına göre yapıyor (renk, boşluk, ekran düzeni seçiyor), mimariyi kafasına göre kuruyor ve test etmediği şeye "çalışıyor" diyor. Kural yazmak bunu çözmedi, çünkü uyulup uyulmadığı görünmüyor. Bu skill'de her şey **script'in saydığı bir sayıdır**:

| Ne | Nasıl ölçülebilir hale gelir | Metrikler |
|---|---|---|
| Tasarım | Kullanıcının tasarımı → `tasarim.json` (renk, font, yazı, boşluk, köşe, bileşen ölçüleri) + `ekranlar.json` (her ekranda her bileşenin sırası, konumu, boyutu) + `tasarim/<ekran>.png` | T1–T6 |
| Yazılım mimarisi | Onaylı mimari → `mimari.json` (katmanlar, izinli bağımlılıklar, satır sınırları) | Y1–Y4 |
| İşlev ve kalite | Cevaplar → `kabul_kriterleri.json` (F, P, K, A, O, U, M) | katalog |
| Claude'un davranışı | `kararlar.json` + onay kanıtı + test adları + teslim mesajı | D1–D5 |

Davranış metrikleri (hepsi == 0, raporda otomatik, çıkarılamaz — D4 mesaj kapısıdır):

| ID | Metrik | Nasıl sayılır |
|---|---|---|
| D1 | Kaynaksız karar (varsayım) | Kullanıcıya bağlanmayan her paket, karar, kriter (`denetim.py kontrol`) |
| D2 | Onaysız yazılmış kod dosyası | Onay kanıtı yokken var olan `.dart/.py/.kt` |
| D3 | Testi olmayan F kriteri | F kriterinin test dosyası diskte yok |
| D5 | ID'siz test | Adında kriter/karar ID'si olmayan test = kayda geçmemiş davranış |
| D4 | Kanıtsız iddia | Ölçüm tamamlanmamışken mesajdaki "bitti/hazır/çalışıyor…" (`denetim.py mesaj`) |

## Akış

```
1. SORU + TASARIM İSTE → 2. KRİTER, TASARIM, MİMARİ, KARAR DOSYALARI → ("Onaylıyorum")
→ 3. UYGULAMA (adım adım) → 4. ÖLÇÜM → 5. EKRAN GÖRÜNTÜSÜ ONAYI → 6. TESLİM
                    ↑_____________ KALDI varsa düzelt _____________|
```

Aşama atlanmaz. Onay yoksa kod yok (D2). Tasarım yoksa kod yok.

## Aşama 1 — Soru turu ve tasarımı isteme

1. `references/soru-bankasi.md`'yi oku. Kullanıcının **açıkça yazdıklarını** bir tabloda geri yansıt ("bunları tekrar sormuyorum"), kalanları sor. Kullanıcının yazmadığı her değer bilinmiyordur; çıkarım = varsayım = D1.
2. **Tasarımı iste.** `references/tasarim.md` §1'deki kontrol listesini kullanıcıya ver: ekran PNG'leri (aynı çerçeve boyutu), renkler, font dosyaları, yazı stilleri, boşluk ölçeği, köşeler, bileşen ölçüleri, her bileşenin konum/boyutu, tolerans, T5 piksel farkı eşiği. Tasarım değeri **önerme**, PNG'den göz kararı çıkarma; eksik olan her değer bir sorudur.
3. **Mimariyi sor.** Kullanıcının kendi mimarisi var mı? Yoksa `references/mimari.md`'deki örnek mimariyi (klasör ağacı + katman kuralları) "(öneri)" olarak göster; dosya/fonksiyon satır sınırlarını sor.
4. Soruları numarala (S1, S2…), seçenek sun, cevabın dönüşeceği metriği yaz (ör. "→ T4 sonucKarti.ust"). Bir turda ~15 soru; mimariyi ve tasarımı belirleyenler önce.
5. Bu aşamada kod, iskelet, `flutter create` yok.

İşlev ve kalite eşiklerinde (P, K, U…) kullanıcı "sen seç" derse somut değer "(öneri)" olarak sunulabilir; kabul ederse kaynak `öneri-onaylandı:Sx`. **Tasarım değerlerinde öneri yoktur** — kaynakları yalnızca `kullanici:` olabilir.

## Aşama 2 — Dosyalar ve onay

Proje köküne yaz (şablonlar `assets/ornek-proje/` içinde, çalışan ve ölçülmüş hâlleriyle):

| Dosya | İçerik | Doğrulama |
|---|---|---|
| `kabul_kriterleri.json` | Tüm kriterler; **T1–T6 ve Y1–Y4 zorunlu** (blok: `assets/ty_kriterleri.ornek.json`) | `kriterler.py dogrula` |
| `tasarim.json`, `ekranlar.json`, `tasarim/<ekran>.png` | Kullanıcının tasarımı, sayı olarak | `tasarim.py dogrula` |
| `mimari.json` | Katmanlar, izinli bağımlılıklar, sınırlar | `mimari.py dogrula` |
| `kararlar.json` | Ölçülmeyen kararlar (paketler, davranışlar); şablon `assets/kararlar.ornek.json` | `denetim.py kontrol` |

Metrikler ve ölçüm komutları: `references/metrik-katalogu.md`. Her kriter: `id, kategori, metrik, operator, esik (sayı), birim, olcum_yontemi, olcum_ortami, kaynak`. Her F kriterinin `olcum_yontemi` test dosyasının yolunu içerir. `flutter create`'in eklediği paketler de karardır (`cupertino_icons`, `flutter_lints`).

Kullanıcıya şunları göster ve "Onaylıyorum" bekle:

```bash
python <skill>/scripts/kriterler.py tablo kabul_kriterleri.json
python <skill>/scripts/tasarim.py tablo --proje .        # tasarım değerleri + her ekranın bileşen tablosu
```
+ mimari klasör ağacı ve katman kuralları + karar listesi.

> Bu kriterleri, tasarım tablosunu, mimariyi ve kararları onaylıyor musun? "Onaylıyorum" yazarsan uygulamaya geçerim. Değiştirmek istediğin satırı ID ile yaz.

Onay gelince `kabul_kriterleri.json` → `onay.durum = "onaylandi"`, `onay.tarih`, `onay.kanit = <kullanıcının cümlesi aynen>`.

## Aşama 3 — Uygulama (işi sonuna kadar yap)

`references/mimari.md` §4'teki **12 adımı sırayla** uygula; her adımın komutu temiz geçmeden sonrakine geçme. Özet:

1. İskelet (`flutter create`), onaysız şablon paketlerini çıkar.
2. Dosyaları doğrula. 3. Fontları `assets/fonts/` + `pubspec.yaml`. 4. `python <skill>/scripts/tasarim.py uret --proje .`
5. Çekirdek tema (yalnızca `Tasarim*` sabitleri). 6. Alan (saf Dart) + ID'li testler → Y1 = 0. 7. Veri. 8. Sunum: her bileşene `ValueKey('<ekran>.<bilesen>')`, değerler yalnızca `Tasarim*` → `flutter test test/yerlesim` T4 = 0. 9. Giriş. 10. Python `tools/`.
11. Ekran görüntüleri → Aşama 5. 12. Ölçüm.

Kurallar:
- Tasarımda olmayan bir değer gerekirse (T4 bir farkı gösterir ve hiçbir `Tasarim*` sabiti kapatmaz) **sor**; sayı yazma (T2), renk yazma (T1), üretilmiş dosyayı düzenleme (T3).
- Kriterlerde/kararlarda olmayan paket veya davranış gerekirse dur ve sor; cevabı `kararlar.json`'a ekle. Kullanıcıya ulaşılamıyorsa en dar seçeneği uygula, `öneri-bekliyor:Sx` olarak kaydet, teslimde sor — D1 bilerek KALDI olur; kaydetmeden uygulamak gizli varsayımdır.
- Her testin adı doğruladığı kriter/karar ID'sini taşır (`test('F1 cevir: 5 km → 5000 m', …)`, `def test_f4_…`) — D5.
- Offline: release manifestinde `INTERNET` yok; ağ kullanan paket (`google_fonts`, analitik) yok; fontlar gömülü.
- Kapsam dışı "iyileştirme" ekleme; önce sor.

## Aşama 4 — Ölçüm

```bash
python <skill>/scripts/olc.py --proje . --cikti olcumler.json [--python-klasoru tools] [--model assets/x.tflite] [--build-apk]
python <skill>/scripts/denetim.py kontrol --proje .
python <skill>/scripts/kriterler.py rapor kabul_kriterleri.json olcumler.json > rapor.md
```

`olc.py` kod kalitesini, F testlerini (her kriter yalnızca kendi ID'li testleriyle), tasarımı (T1–T6: statik tarama, yerleşim testleri, ekran görüntüsü ↔ tasarım PNG piksel farkı, onaylı görüntü sapması) ve mimariyi (Y1–Y4) ölçer. Araç/cihaz/veri yoksa `null` + sebep yazar — tahmini değer yazmaz. Cihaz gerektirenleri katalogdaki komutlarla ölç, `{"deger": x, "kanit": "<komut çıktısı>"}` ekle; ölçemiyorsan `{"deger": null, "sebep": "…"}`.

`KALDI` varsa düzelt, yeniden ölç. Eşik değiştirmek yalnızca kullanıcının kararıdır (`surum` artar).

## Aşama 5 — Ekran görüntüsü onayı

1. `test/goruntu/olcum/<ekran>.png` (uygulamanın görüntüsü), `tasarim/<ekran>.png` (kullanıcının tasarımı) ve `build/tasarim_fark/<ekran>.png` (kırmızı = farklı piksel) görüntülerini kullanıcıya göster, T5 yüzdesini yaz.
2. Kullanıcı onaylarsa: `flutter test --update-goldens test/goruntu` → `goldens/` (T6 artık her görsel değişikliği yakalar). Onay yoksa golden üretme; T6 ÖLÇÜLEMEDİ kalır.

## Aşama 6 — Teslim

`yanit.md`, bu yapıyla:

```markdown
## Teslim raporu
**DURUM:** <rapor.md'nin son satırı, aynen>

### Ölçüm tablosu
<rapor.md içeriği, aynen>

### Yapılanlar
<dosyalar, her biri hangi kriter için>

### Ölçülemeyenler
<her ÖLÇÜLEMEDİ: neden + kullanıcının çalıştıracağı komut>

### Açık sorular / sapmalar
<öneri-bekliyor kararlar, tasarımda eksik çıkan değerler; yoksa "Yok">
```

```bash
python <skill>/scripts/denetim.py mesaj yanit.md --kriterler kabul_kriterleri.json --olcumler olcumler.json
```

D4 > 0 ise gönderme: iddiayı sayıyla değiştir ("çalışıyor" → "K4: 12 testin 12'si geçti"), özet satırını ekle, tekrar denetle.

## Kısa örnek

**Kullanıcı:** "İnternetsiz çalışan bir birim çevirici yap."

**Yanlış:** Yeşil bir tema seçip, 16 dp boşluklarla, Provider ile tek ekran yazmak ve "hazır" demek. Sonuç: D1 = 1, D2 = 9 dosya, T1/T2 > 0 (renk ve ölçü uyduruldu), D4 = 1.

**Doğru:** S1–S15 + tasarım kontrol listesi → kullanıcı Figma'dan değerleri ve PNG'yi verir → dosyalar → onay → 12 adım → ölçüm → ekran görüntüsü onayı → `DURUM: TAMAM — 21 kriter GEÇTİ` (bkz. `assets/ornek-proje/rapor.md`).

## Dosyalar

- `references/soru-bankasi.md` — Sorular ve hangi metriğe dönüştükleri. Aşama 1.
- `references/tasarim.md` — Tasarımı isteme, dosyalara dökme, eksik değer, T1–T6, sık hatalar.
- `references/mimari.md` — Örnek mimari, katman kuralları, 12 kurulum adımı, Y1–Y4.
- `references/metrik-katalogu.md` — Tüm metrikler, birimler, komutlar, sık teknik hatalar.
- `assets/ornek-proje/` — Çalışan, ölçülmüş tam örnek (21/21 GEÇTİ).
- `assets/kabul_kriterleri.ornek.json`, `assets/ty_kriterleri.ornek.json`, `assets/kararlar.ornek.json` — Şablonlar.
- `scripts/kriterler.py` (`dogrula`, `tablo`, `rapor`), `scripts/olc.py` (tüm otomatik ölçümler), `scripts/denetim.py` (`kontrol` D1–D5, `mesaj` D4), `scripts/tasarim.py` (`dogrula`, `uret`, `tablo`, `denetle`), `scripts/mimari.py` (`dogrula`, `denetle`), `scripts/goruntu_karsilastir.py` (PNG piksel farkı + fark görüntüsü).
