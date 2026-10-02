240 öğrencinin verisiyle dört iddiayı test ettim. Hocanın ikisi tutuyor, ikisi tutmuyor.

| # | İddia | Sonuç | Ne buldum | İddianın doğru olma olasılığı* |
|---|---|---|---|---|
| 1 | Çok çalışanın notu yüksek | **Tutuyor (güçlü)** | r = 0.59. Haftada +1 saat çalışma ≈ +1.4 puan. En az çalışan %25'in ortalaması 69.5, en çok çalışan %25'in 87.5 | ≈ %100 |
| 2 | Sosyal medya notu düşürüyor | **Tutuyor (orta-zayıf)** | r = −0.24. Günde +1 saat ≈ −2.5 puan, uyku hesaba katılınca −1.6 puan (p = 0.009) | ≈ %99.6 (kontrollü) |
| 3 | Kızlar erkeklerden başarılı | **Tutmuyor** | Kızlar 78.7, erkekler 80.6 (p = 0.22). Anlamlı bir fark yok | ≈ %11 |
| 4 | Uykunun notla alakası yok | **Tutmuyor (iddia yanlış)** | r = +0.26. +1 saat uyku ≈ +2.2 ile +3.3 puan. 6 saatten az uyuyanların ortalaması 74.4, 8 saatten fazla uyuyanların 82.9 | "Alakası yok" olasılığı ≈ %0.4 (kontrollü ≈ %14) |

\* Bunlar bilgisiz bir başlangıç varsayımıyla hesaplanmış Bayesçi olasılıklar. p-değeri değiller; p-değerleri de raporda var. Dört test birlikte düzeltildiğinde (Holm) de 1, 2 ve 4 anlamlı kalıyor, 3 anlamlı değil.

**Toplantıda işine yarayacak ayrıntılar:**
- **Sosyal medya ile uyku birbirine bağlı.** Çok sosyal medya kullananlar daha az uyuyor (r = −0.51). Sosyal medyanın nottaki "etkisinin" yaklaşık üçte biri uykuyla örtüşüyor. Yine de ikisi de tek başına anlamlı kalıyor. Sosyal medya ile çalışma saati arasında ise hiç ilişki yok.
- **Kız-erkek konusunda veri iddianın tersine hafifçe eğilimli ama fark anlamlı değil.** Doğru ifade "fark yok" olur. Bayes faktörü "fark yok"u yaklaşık 7'ye 1 destekliyor.
- **"Düşürüyor" nedensel bir iddia.** Bu veri gözlemsel, bu yüzden yalnızca birlikte değişim gösterebiliyor. Neden-sonuç ilişkisi bu veriyle kanıtlanamaz. Bu uyarı 1. iddia için de geçerli.
- **Sonuçlar sağlam.** Notu 100'de tavan yapan 11 öğrenciyi çıkarınca da sonuçlar değişmiyor. Parametrik olmayan testler ve bootstrap da aynı sonucu veriyor.

**Yaptığım varsayımlar:**
- Not 0–100 ölçeğinde kabul edildi.
- K = kız, E = erkek olarak okundu.
- Eksik değerleri (sosyal medyada 6, uykuda 9 tane) yalnızca ilgili analizden çıkardım.

**Kaydedilen dosyalar** (`iteration-1/ogrenci-verisi-iddialari/without_skill/outputs/` içinde):
- `rapor.md`: tablolar ve yöntem notlarıyla tam rapor
- `sonuclar.json`: bütün istatistikler
- `analiz.py`: analizi tekrar çalıştırmak için betik
