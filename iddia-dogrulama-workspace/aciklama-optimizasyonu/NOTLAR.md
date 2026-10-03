# Açıklama optimizasyonu — notlar

- Değerlendirme seti: `tetikleme_eval.json` (10 tetiklenmeli, 10 tetiklenmemeli; yakın konulu negatifler).
- **İlk deneme geçersiz sayıldı.** skill-creator'ın `run_eval.py` betiği paralel işçilerin hepsinin geçici
  komut dosyasını aynı `.claude/commands/` klasörüne yazıyor. Model ~10 özdeş kopyadan birini seçiyor;
  başka işçinin kopyasını seçince sorgu "tetiklenmedi" sayılıyor. Sonuç: ~%11 sahte recall (≈1/10).
- Düzeltme: her sorgu kendi geçici proje kökünde (`tempfile.mkdtemp`) çalıştırıldı (yerel kopyada yama).
- Düzeltilmiş ölçüm:
  - Tek seferlik kontrol (`tek_seferlik_kontrol.json`): 19/20.
  - Optimizasyon döngüsü (her sorgu 3 kez, %60 eğitim / %40 test): eğitim 36/36, test 24/24 —
    **mevcut açıklama tüm sorgularda doğru**; döngü 1. turda `all_passed` ile durdu, açıklama değiştirilmedi.
- Tek seferlik kontroldeki tek kaçırma ("3 farklı rapor…") 3 tekrarlı ölçümde 3/3 tetiklendi; gürültüydü.
