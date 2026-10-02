İddianın iki iddialı kısmı da literatürle desteklenmiyor. Kanıtlar, faydanın büyük ölçüde daha az kalori alınmasından geldiğini gösteriyor; yemek saatlerinin kendisinin etkisi yok gibi görünüyor. İddiayı 8 parçaya ayırdım (asıl iddialar, rakipleri ve daha zayıf halleri) ve 18 farklı yayından 43 kanıt kaydı ile puanladım. Konu sağlık olduğu için karar eşiklerini sıkılaştırdım: kabul için olasılığın en az 0.95, koşullu kabul için en az 0.80 olması gerekiyor.

Tabloda S, kanıtların ortalama yönünü gösteriyor (−1 tamamen karşı, +1 tamamen destekliyor). P, iddianın doğru olma olasılığı. Sağlamlık, önsel ve kanıtlar arası bağımlılık varsayımlarını değiştirdiğim 27 senaryonun kaçında kararın aynı kaldığını gösteriyor.

| ID | İddia | S | P | Karar | Sağlamlık |
|---|---|---|---|---|---|
| C1 | Aynı kaloride 16:8 daha fazla kilo verdirir | −0.25 (zayıf çelişki) | 0.10 | Büyük olasılıkla yanlış | %33 |
| C2 | …"çok daha fazla" (klinik olarak anlamlı) kilo verdirir | −0.68 (güçlü çelişki) | 0.012 | **Ret** | %78 |
| C3 | *Rakip:* aynı kaloride kilo kaybı farkı yok | +0.29 (zayıf destek) | 0.87 | Koşullu kabul | %52 |
| C4 | *Zayıf hali:* 16:8, hiçbir diyet yapmamaya göre kilo verdirir | +0.49 (orta destek) | 0.82 | Koşullu kabul | %33 |
| C5 | 16:8 insülin direncini azaltır (hiçbir şey yapmamaya göre) | +0.19 (zayıf destek) | 0.73 | Belirsiz | %56 |
| C6 | Aynı kaloride klasik diyetten daha çok azaltır | −0.30 (orta çelişki) | 0.15 | Büyük olasılıkla yanlış | %48 |
| C7 | *Rakip:* aynı kaloride insülin direncinde fark yok | +0.30 (orta destek) | 0.78 | Belirsiz | %41 |
| C8 | İnsülin direncini **tamamen** düzeltir | −0.44 (orta çelişki) | 0.010 | **Ret** | %67 |

**Kilo kaybı:**
- Kalorinin gerçekten eşitlendiği kontrollü besleme deneyinde (Maruthur 2024, Annals of Internal Medicine) 16:8'e benzer grup biraz daha **az** kilo verdi: −2.3 kg, karşılaştırma grubunda −2.6 kg.
- En kapsamlı iki derleme de klasik diyete göre üstünlük bulmadı. BMJ 2025 ağ meta-analizi 99 randomize deneyi, Cochrane 2026 derlemesi 22 randomize deneyi kapsıyor.
- 16:8, hiçbir şey yapmamaya göre kilo verdiriyor, ama bunun nedeni insanların kendiliğinden günde yaklaşık 400–550 kcal daha az yemesi.

**İnsülin direnci:**
- Hiçbir kaynak insülin direncinin normale döndüğünü bildirmiyor.
- Görülen iyileşmeler küçük ve koşullu: yalnızca fazla kilolularda (obezlerde değil) ya da yalnızca 6 aydan uzun süren çalışmalarda görülüyor.
- Kalori eşitken saatin kendi etkisini destekleyen tek güçlü çalışma çok küçük: Sutton 2018, 8 erkek. Üstelik 16:8 değil, 6 saatlik erken bir pencere kullanılmış.

**Güvenilirliği sınırlayan iki nokta:**
1. **Tam metinleri okuyamadım.** Ağ politikası PubMed, NEJM, JAMA, BMJ, Cochrane gibi yayın sitelerini açmamı engelledi. Kaynakların var olduğunu ve bulgularını yalnızca arama özetlerinden doğrulayabildim. Bu yüzden her kaynağın güvenilirlik puanı (0–1 arası kalite puanı) %30 düşürüldü; ortalama kalite "Orta" (0.51–0.60). Tam metinlerle sonuçların yönü değişmez ama değerler daha uca kayabilir.
2. **Kararların bandı kesin değil.** C1, C3–C8 sağlamlık eşiğinin (%70) altında kaldı. Kararların yönü (iddia lehine değil) senaryoların çoğunda korunuyor; ama hangi banda düştükleri kesin değil. Örneğin C1'in P değeri senaryolara göre 0.015 ile 0.52 arasında değişiyor.

Ayrıca, diyabet ilacı kullananlar bu ifadeye güvenip ilacı bırakmamalı. Uzun açlık süreleri bu kişilerde kan şekerinin tehlikeli düşmesine (hipoglisemi) yol açabilir; başlamadan önce hekime danışılmalı.

Dosyalar şu klasörde: `/home/user/calisma-alanim/iddia-dogrulama-workspace/iteration-1/aralikli-oruc-literatur/with_skill/outputs/`
- `rapor.md`: tam rapor; her kaynağın puanı, alıntısı ve gerekçesi, yorum ve öneriler bölümüyle birlikte.
- `metadata.json`: tüm puanlar, duyarlılık analizi ve uyarılar.
- `girdi.json`: kodlanmış iddialar ve kanıtlar.
- `girdi_olusturucu.py`: girdi dosyasını yeniden üreten betik.
