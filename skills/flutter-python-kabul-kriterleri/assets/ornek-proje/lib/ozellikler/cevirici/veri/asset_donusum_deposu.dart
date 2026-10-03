import 'dart:convert';

import 'package:flutter/services.dart';

import '../alan/birim_donusumu.dart';
import '../alan/donusum_deposu.dart';

/// Python script'inin ürettiği assets/birimler.json dosyasını okur (offline).
class AssetDonusumDeposu implements DonusumDeposu {
  @override
  Future<List<BirimDonusumu>> hepsi() async {
    final metin = await rootBundle.loadString(
      'assets/birimler.json',
      cache: false,
    );
    final liste = jsonDecode(metin) as List<Object?>;
    return [
      for (final o in liste) BirimDonusumu.jsondan(o! as Map<String, Object?>),
    ];
  }
}
