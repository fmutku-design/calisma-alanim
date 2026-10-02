**Üç taraftan hiçbiri tam olarak haklı değil. Veriye en yakın duran İK, ama "hiçbir ilişki yok" demek fazla kesin.**

**Asıl bulgu: ilişkiyi kıdem yaratıyor.** Ham veride uzaktan gün sayısı arttıkça verimlilik de artıyor. 0 gün çalışanların ortalaması 58,6 puan, 5 gün çalışanlarınki 75,5 (r = 0,44). Ama uzaktan gün arttıkça ortalama kıdem de 2,4 yıldan 11,4 yıla çıkıyor. Kıdemli çalışanlar hem daha çok uzaktan çalışıyor hem daha verimli. Kıdem ve departman sabit tutulunca uzaktan çalışmanın etkisi gün başına −0,66 puana iniyor. Bu fark anlamlı değil (95% güven aralığı −1,8 ile +0,5, p = 0,26). Kıdem bantlarının içinde de korelasyon sıfıra yakın.

**İddia bazında:**
- **Çalışanlar ("artırıyor"): Desteklenmiyor.** Gördükleri ilişki gerçek ama nedensel değil, kıdemden geliyor. Bu ilişki dört departmanın hepsinde var ama kıdem hesaba katılınca hepsinde kayboluyor.
- **Genel müdür ("düşürüyor"): Genel hâliyle desteklenmiyor.** Yalnızca haftada 5 gün uzaktan çalışan 12 kişilik grupta yaklaşık −7 puanlık zayıf bir düşüş işareti var (p ≈ 0,04–0,07). Grup küçük ve birçok karşılaştırma yapıldı. Bu yüzden bu bir kanıt değil, test edilmesi gereken bir hipotez.
- **İK ("hiçbir ilişki yok"): Kısmen doğru.** Ham veride bir ilişki var. Nedensel bir etki ise görülmüyor. Ama veri "etki sıfır" demeye de yetmiyor: haftada 5 gün için −9 ile +2,5 puan arasındaki etkiler dışlanamıyor.

**Uyuşuyorlar mı?** Genel müdür ile çalışanlar doğrudan çelişiyor. İK ikisiyle de çelişiyor. Ama aslında farklı şeylere bakıyorlar: çalışanlar ham ilişkiye, İK kıdem ve departman hesaba katılmış (kontrollü) ilişkiye, genel müdür ise belki tamamen uzaktan çalışmaya. Bu açıdan bakınca kısmen uzlaştırılabilirler.

**İK'nın gönderdiği kaynaklar:**
- **Bloom ve ark. 2015 (QJE):** Doğrulandı. Ctrip'in Şanghay çağrı merkezinde 249 gönüllüyle yapılmış rastgele bir deney. Haftada 4 gün evden çalışanların performansı %13 artmış. Bu güçlü bir nedensel kanıt, ama rutin ve kolay ölçülen çağrı merkezi işi için. Yazılım, satış ve finans gibi işlere doğrudan taşınamaz. Aynı ekibin 2024 tarihli *Nature* deneyi (1.612 kişi, haftada 2 gün hibrit) performansta **etki bulmuyor**, ayrılmalarda ise üçte bir azalma buluyor. Bu bizim kontrollü sonucumuzla uyumlu.
- **2023 dergi anketi (yöneticilerin %60'ı):** Verimliliği değil, yönetici **kanaatini** ölçüyor ve çalışanlara sorulmamış. Haberin kaynağı belirtilmediği için doğrudan doğrulayamadım. Benzer bir rakam Owl Labs'ın 2023 raporunda geçiyor. Genel müdürün iddiasına kanıt değil, yaygın bir algının göstergesi.
- **İki kaynak birbiriyle çelişmiyor:** biri ölçülen performansı, diğeri algıyı ölçüyor.

**Kurula önerim:**
- Ham karşılaştırmalarla karar vermeyin.
- Hibrit düzenin (1–3 gün) verimliliğe zarar verdiğine dair kanıt yok.
- Tamamen uzaktan çalışmayı temkinle izleyin.
- Kesin cevap için bir veya iki departmanda uzaktan gün sayısını kura ile atadığınız 3–6 aylık bir pilot yapın.

**Varsayımlar ve sınırlar:**
- Verimlilik puanının nesnel olduğunu varsaydım. Nasıl ölçüldüğü bilinmiyor; yönetici değerlendirmesiyse yanlı olabilir.
- Veri gözlemsel ve tek bir zaman noktasına ait. Performansı yüksek olanlara daha çok uzaktan gün hakkı veriliyor olabilir.
- 4–5 gün grupları küçük (19 ve 12 kişi).

**Dosyalar** (`.../without_skill/outputs/` klasöründe):
- `rapor.md`: Kurul için tam rapor.
- `iddia_degerlendirme.json`: İddia bazında hüküm özeti.
- `sonuclar.json` ve `ek_sonuclar.json`: Tüm sayısal sonuçlar.
- `analiz.py` ve `ek_analiz.py`: Analizi yeniden üreten betikler (yalnızca Python standart kütüphanesi).
