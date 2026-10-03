import 'birim_donusumu.dart';

/// [kaynak] → [hedef] dönüşümü; ters yön çarpana bölünerek hesaplanır. Tanımsızsa null.
double? cevir(
  double deger,
  String kaynak,
  String hedef,
  List<BirimDonusumu> tablo,
) {
  for (final d in tablo) {
    if (d.kaynak == kaynak && d.hedef == hedef) return deger * d.carpan;
    if (d.kaynak == hedef && d.hedef == kaynak) return deger / d.carpan;
  }
  return null;
}

/// [kaynak] biriminden gidilebilen hedef birimler (doğrudan ve ters).
List<String> hedefler(String kaynak, List<BirimDonusumu> tablo) => [
  for (final d in tablo)
    if (d.kaynak == kaynak) d.hedef else if (d.hedef == kaynak) d.kaynak,
];
