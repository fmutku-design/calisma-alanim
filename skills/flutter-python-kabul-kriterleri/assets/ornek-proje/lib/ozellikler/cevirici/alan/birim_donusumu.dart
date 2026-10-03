/// Bir dönüşüm satırı: 1 [kaynak] = [carpan] [hedef].
class BirimDonusumu {
  const BirimDonusumu({
    required this.kategori,
    required this.kaynak,
    required this.hedef,
    required this.carpan,
  });

  factory BirimDonusumu.jsondan(Map<String, Object?> json) => BirimDonusumu(
    kategori: json['kategori']! as String,
    kaynak: json['kaynak']! as String,
    hedef: json['hedef']! as String,
    carpan: (json['carpan']! as num).toDouble(),
  );

  final String kategori;
  final String kaynak;
  final String hedef;
  final double carpan;
}
