Danışmanının 4 iddiasını 240 öğrencilik verinde test ettim. Kısaca: **iki iddia tutuyor, ikisi tutmuyor.** Sosyal medya iddiası ise ancak "ilişki var" şeklinde söylenirse tutuyor, "düşürüyor" şeklinde değil.

| # | İddia | Verinde ne çıktı | Olasılık (P) | Karar | Sağlamlık |
|---|---|---|---|---|---|
| 1 | Çok çalışanın notu yüksek | r = 0,59; haftada +1 saat çalışma ≈ +1,4 puan | **0,997** | ✅ Tutuyor (kabul) | %96 |
| 2a | Sosyal medya düşük notla ilişkili | r = −0,24; günde +1 saat ≈ −1,6 puan | **0,974** | ✅ Tutuyor (kabul) | %82 |
| 2b | Sosyal medya notu *düşürüyor* (nedensel) | Veri kesitsel, neden-sonuç gösteremez | 0,848 | ⚠️ Koşullu, kırılgan | %37 |
| 3 | Kızlar erkeklerden daha başarılı | Kızlar 78,7, erkekler 80,6 (fark anlamsız, p = 0,22) | **0,102** | ❌ Büyük olasılıkla yanlış | %44 |
| 4 | Uykunun notla alakası yok | r = 0,26; <6 saat uyuyanlar 73,8, ≥7,5 saat uyuyanlar 83,2 | **0,018** | ❌ Tutmuyor (ret) | %89 |

P, iddianın doğru olma olasılığı. Önce veriye bakmadan bir başlangıç olasılığı belirledim, sonra bunu verideki kanıtla güncelledim. Sağlamlık, varsayımları 27 farklı şekilde değiştirdiğimde kararın kaç senaryoda aynı kaldığını gösteriyor.

**Dikkat etmen gerekenler:**
- **İddia 3:** Verin "erkekler daha başarılı" da demiyor. Doğru yorum, iki grup arasında anlamlı bir fark olmadığı. "Fark yok" iddiasının olasılığı 0,72.
- **İddia 2 ve 4 birbirine bağlı:** Sosyal medya kullanımı arttıkça uyku azalıyor (r = −0,51). Sosyal medyanın notla ilişkisi kısmen uyku üzerinden geçiyor olabilir. Yani danışmanının "sosyal medya notu düşürür" ve "uykunun notla alakası yok" demesi kendi içinde de pek tutarlı değil.
- **Sınırlılık:** Bütün sonuçlar tek bir veri setinden çıktı ve literatür taraması yapmadım. Bu yüzden sonuçlar "bu 240 öğrenci için" geçerli. Bütün iddialarda `insufficient_evidence` uyarısı bu nedenle çıktı.

**Varsayımlarım:** Başarı ölçüsü olarak `not_ortalamasi` sütununu kullandım. Yalnızca 2. iddiayı ("düşürüyor") nedensel kabul ettim, diğerlerini ilişki iddiası olarak ele aldım. Kontrollü analizlerde diğer değişkenleri, cinsiyeti ve okul türünü sabit tuttum. Sıralamaya dayalı korelasyonla (Spearman) yaptığım kontrol aynı sonuçları verdi.

**Dosyalar** (`/home/user/calisma-alanim/iddia-dogrulama-workspace/iteration-1/ogrenci-verisi-iddialari/with_skill/outputs/`):
- `rapor.md`: tam rapor. Yorum, sınırlılıklar ve uygulama önerileri burada.
- `metadata.json`: bütün sayılar ve duyarlılık analizi.
- `girdi.json`: iddialar, başlangıç olasılıkları ve test sonuçları. Analizi aynı şekilde tekrarlamak için bu dosya yeterli.
