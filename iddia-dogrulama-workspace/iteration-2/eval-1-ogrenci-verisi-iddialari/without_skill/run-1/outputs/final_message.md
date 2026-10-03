Dört iddiayı 240 öğrencilik verinle test ettim. Sonuç: biri net doğru, biri ilişki olarak doğru, ikisi verinle çelişiyor.

| # | İddia | Sonuç | Ne buldum | p | İlişki/fark olma olasılığı* |
|---|---|---|---|---|---|
| 1 | Çok çalışanın notu yüksek | **Tutuyor (çok güçlü)** | r = 0,59. Haftada her ek çalışma saati ≈ +1,4 puan. En az çalışan çeyrek 69,5, en çok çalışan 87,5 | 5×10⁻²⁴ | > %99,99 |
| 2 | Sosyal medya notu düşürüyor | **İlişki tutuyor, "düşürüyor" kanıtlanamaz** | r = −0,24. Günde her ek saat ≈ −2,5 puan; diğer değişkenler sabitken −1,6 puan | 0,00016 | ≈ %98,5 |
| 3 | Kızlar erkeklerden başarılı | **Tutmuyor** | Kızlar 78,7, erkekler 80,6. Yön bile ters ama fark anlamsız (−1,9 puan, %95 GA [−5,0; +1,2]) | 0,22 | Fark var: ≈ %22. Kızların önde olma olasılığı ≈ %11 |
| 4 | Uykunun notla alakası yok | **Tutmuyor** | r = 0,26. Her ek saat uyku ≈ +3,3 puan. 6 saatten az uyuyanlar 73,8, 8 saat ve üzeri uyuyanlar 83,2 | 0,00006 | İlişki var: ≈ %99,4 |

\*Bu sütun Bayes faktöründen geliyor; başta "ilişki var" ve "yok" ihtimallerine %50–%50 verdim. p değeri iddianın doğru olma olasılığı değil, o yüzden ikisini birlikte verdim.

**Hocayla konuşurken işine yarayacak noktalar:**
- **Sosyal medya:** Verin kesitsel, yani ilişkiyi gösteriyor ama neden-sonucu göstermiyor. Notu düşük olan öğrenci sosyal medyaya daha çok kaçıyor da olabilir. Bir de şu var: sosyal medya uykuyla güçlü biçimde ters ilişkili (r = −0,51), çalışma süresiyle ise hiç ilişkili değil. Yani olası zararın bir kısmı uykuyu azaltması üzerinden geliyor gibi.
- **Cinsiyet:** Veri "fark yok" tarafını yaklaşık 3,5 kat daha çok destekliyor. Okul türü ya da diğer değişkenler sabit tutulunca da sonuç değişmiyor.
- **Uyku:** Çalışma ve sosyal medya sabit tutulunca da etki sürüyor (+2,2 puan/saat, p = 0,002). Çok uyumanın zararlı olduğuna dair bir işaret de bulmadım.
- Dört test birlikte yapıldığı için çoklu karşılaştırma düzeltmesi (Holm) uyguladım; kararlar değişmedi. Notu tam 100 olan 11 öğrenciyi çıkarınca da değişmedi.

**Varsaydıklarım:**
- `K` kız, `E` erkek; notlar 0–100 ölçeğinde.
- Sosyal medyada 6, uykuda 9 eksik değer vardı. Bu öğrencileri sadece ilgili analizden çıkardım; tüm değişkenleri birlikte kullanan modelde 226 öğrenci kaldı.

**Dosyalar** (`iteration-2/eval-1-ogrenci-verisi-iddialari/without_skill/run-1/outputs/` içinde):
- `rapor.md`: ayrıntılı rapor (tablolar, güven aralıkları, sınırlılıklar)
- `analiz_sonuclari.json`: bütün sayılar
- `analiz.py`: analizi baştan üreten betik
