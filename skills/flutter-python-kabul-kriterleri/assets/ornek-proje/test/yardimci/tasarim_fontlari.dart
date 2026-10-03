// ÜRETİLMİŞ DOSYA — elle düzenleme. Kaynak: tasarim.json (scripts/tasarim.py uret)
import 'dart:io';

import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

/// Testlerde gerçek fontları yükler. Yüklenmezse Flutter testleri yazıları kutu (Ahem) olarak çizer
/// ve yerleşim/ekran görüntüsü ölçümleri tasarımla karşılaştırılamaz.
Future<void> tasarimFontlariniYukle() async {
  TestWidgetsFlutterBinding.ensureInitialized();
  await (FontLoader('Roboto')
        ..addFont(rootBundle.load('assets/fonts/Roboto-Regular.ttf'))
        ..addFont(rootBundle.load('assets/fonts/Roboto-Bold.ttf')))
      .load();
  final ikon = _materialIkonFontu();
  if (ikon != null) {
    final veri = ikon.readAsBytesSync();
    await (FontLoader(
      'MaterialIcons',
    )..addFont(Future.value(ByteData.sublistView(veri)))).load();
  }
}

/// Flutter SDK içindeki Material ikon fontunu bulur (flutter_tester'ın konumundan).
File? _materialIkonFontu() {
  var dizin = File(Platform.resolvedExecutable).parent;
  for (var i = 0; i < 6; i++) {
    final aday = File('${dizin.path}/material_fonts/MaterialIcons-Regular.otf');
    if (aday.existsSync()) return aday;
    dizin = dizin.parent;
  }
  return null;
}
