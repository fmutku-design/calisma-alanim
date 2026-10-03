// ÜRETİLMİŞ DOSYA — elle düzenleme. Kaynak: ekranlar.json (scripts/tasarim.py uret)
import 'dart:io';
import 'package:birimcevirici/cekirdek/tema/tema.dart';
import 'package:birimcevirici/ozellikler/cevirici/sunum/cevirici_ekrani.dart';
import 'package:birimcevirici/ozellikler/cevirici/veri/asset_donusum_deposu.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import '../yardimci/tasarim_fontlari.dart';

/// Varsayılan: onaylı ekran görüntüsüyle (goldens/) birebir karşılaştırma (T6).
/// Ölçüm: --update-goldens --dart-define=GORUNTU_KLASORU=olcum ile güncel görüntü olcum/ altına yazılır,
/// sonra goruntu_karsilastir.py kullanıcının tasarım görseliyle karşılaştırır (T5).
const _klasor = String.fromEnvironment(
  'GORUNTU_KLASORU',
  defaultValue: 'goldens',
);

void main() {
  setUpAll(tasarimFontlariniYukle);

  Future<void> ac(WidgetTester tester) async {
    tester.view.physicalSize = const Size(360, 800);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.reset);
    await tester.pumpWidget(
      MaterialApp(
        debugShowCheckedModeBanner: false,
        theme: uygulamaTemasi(),
        home: CeviriciEkrani(depo: AssetDonusumDeposu()),
      ),
    );
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 500));
  }

  final onayli = File('test/goruntu/goldens/cevirici.png');
  testWidgets(
    'T6 cevirici: ekran görüntüsü',
    (tester) async {
      await ac(tester);
      await expectLater(
        find.byType(MaterialApp),
        matchesGoldenFile('$_klasor/cevirici.png'),
      );
    },
    skip:
        _klasor == 'goldens' && !onayli.existsSync() && !autoUpdateGoldenFiles,
  );
}
