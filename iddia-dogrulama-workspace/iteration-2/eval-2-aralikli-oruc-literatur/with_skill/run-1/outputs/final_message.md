Sitedeki iddiayı beş parçaya ayırıp her birini literatürle karşılaştırdım. Kısa cevap: iddianın iki iddialı kısmı yanlış. 16:8, aynı kaloriyi alan klasik diyetten "çok daha fazla" kilo verdirmiyor ve insülin direncini "tamamen" düzeltmiyor. Ölçülü bir doğru tarafı da var: 16:8, insanların daha az yemesini sağladığı için insülin direncini biraz azaltabilir.

**İddianın parçaları**

Her satırda iki sayı var. S, kaynakların ortalamada iddiayı ne kadar desteklediğini gösteriyor (−1 ile +1 arası). P, iddianın doğru olma olasılığı.

| Parça | S | P | Karar | Sağlamlık |
|---|---|---|---|---|
| C1 · Aynı kaloride daha fazla kilo verdirir | −0.12 | **0.12** | Büyük olasılıkla yanlış | %33 (kırılgan) |
| C4 · Aynı kaloride **çok** daha fazla kilo verdirir | −0.63 | **0.003** | Ret | %93 |
| C11 · İnsülin direncini **tamamen** düzeltir | −0.50 | **0.008** | Ret | %70 |
| C5 · Aynı kaloride insülin direncini daha çok düşürür | −0.41 | 0.02 | Ret | %85 |
| C8 · Normal beslenmeye göre insülin direncini *azaltır* | +0.25 | 0.75 | Belirsiz | %63 |
| Karşı görüş C3 · Aynı kaloride kilo farkı yok | +0.16 | 0.85 | Koşullu kabul | %56 |
| Karşı görüş C6 · Aynı kaloride insülin direnci farkı yok | +0.41 | 0.97 | Kabul | %59 |

Sağlamlık, analizdeki varsayımlar değiştirildiğinde kararın kaç senaryoda aynı kaldığını gösteriyor.

**Kaynaklar ne diyor**
- **Kilo:** Kalori gerçekten eşitlendiğinde fark yok. Maruthur 2024'te (Annals) TRE grubu 2.3 kg, karşılaştırma grubu 2.6 kg verdi. TREATY çalışmasında (NEJM 2022) 12 ay sonunda gruplar arası fark 1.8 kg'dı ve istatistiksel olarak anlamlı değildi (P=.11). BMJ 2025'teki 99 RCT'lik ağ meta-analizi de 16:8 benzeri diyetleri klasik kalori kısıtlamasına "benzer" buldu.
- **TRE lehine sonuçlar:** Bazı meta-analizler TRE lehine 1.4–2.1 kg ek kayıp, Jamshed 2022 ise 2.3 kg ek kayıp buldu. Ancak Jamshed'in yazarları bu farkı TRE grubunun günde ~214 kcal daha az yemesine bağlıyor.
- **İnsülin direnci:** 16:8'e özgü en geniş meta-analiz (23 RCT, n=1280) insülin direncinde (HOMA-IR) yalnızca "hafif" bir düşüş buldu (SMD −0.16). Kalorinin sabit tutulduğu ChronoFast 2025 çalışmasında ise insülin duyarlılığı değişmedi. Düzelme veya normalleşme bildiren bir RCT bulamadım.

**Kaynakların güvenilirliği**
Her kaynağa tasarım, örneklem büyüklüğü ve popülasyon uyumuna göre bir kalite puanı (Q, 0–1) verdim. Kullanılan kaynaklar büyük ölçüde RCT ve meta-analiz. Buna rağmen puanlar orta düzeyde kaldı (ortalama Q 0.43–0.59), bunun iki nedeni var:
- Bu ortamda sayfa açma (WebFetch) engelliydi. Kaynakların var olduğunu arama sonuçlarıyla doğruladım ama bulguları makalelerin kendisinden değil, arama özetlerinden aldım. Bu yüzden hepsi "içerik doğrulanmadı" olarak işaretlendi ve puanları düşürüldü.
- Meta-analizler, içerdikleri RCT'lerle kısmen örtüşüyor; aynı çalışma iki kez sayılmış olabilir. Bu yüzden tüm örtüşen kaynakları tek kanıt sayan, en tutucu ikinci bir hesap yaptım. Bu hesapta da "çok daha fazla" (P=0.04) ve "tamamen düzeltir" (P=0.03) reddedildi. Buna karşılık "aynı kaloride fark yok" sonuçları belirsiz bandına indi (P≈0.58–0.68).

**Yaptığım varsayımlar**
- "Klasik diyet" = sürekli günlük kalori kısıtlaması.
- "Çok daha fazla" = vücut ağırlığının %3'ü veya 3 kg'dan fazla ek kayıp.
- "Tamamen düzeltir" = insülin direncinin normal düzeye inmesi.
- Popülasyon = fazla kilolu veya obez yetişkinler.
- Bu bir sağlık iddiası olduğu için karar eşiklerini sıkılaştırdım: "kabul" için P≥0.95 gerekiyor.

Bu analiz tıbbi tavsiye değildir. İnsülin direnci veya diyabeti olanlar ilaçlarını hekim onayı olmadan değiştirmemeli.

**Dosyalar** (`/home/user/calisma-alanim/iddia-dogrulama-workspace/iteration-2/eval-2-aralikli-oruc-literatur/with_skill/run-1/outputs/`)
- `rapor.md`: tam rapor; kaynak tabloları, yorum, uygulama önerileri ve sonraki en değerli kanıt.
- `metadata.json`: tüm skorlar, kalite puanının nasıl hesaplandığı, duyarlılık analizi ve bayraklar.
- `girdi.json`: iddialar ve 34 kanıt kaydı; kaynak künyeleri, alıntılar ve doğrulama notları burada. `girdi_olustur.py` bu dosyayı yeniden üretir.
- `varyant_tek_kume/`: tüm örtüşen kaynakları tek kanıt sayan tutucu hesap.
