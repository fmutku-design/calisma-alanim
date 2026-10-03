import 'package:birimcevirici/cekirdek/tema/tema.dart';
import 'package:birimcevirici/ozellikler/cevirici/alan/birim_donusumu.dart';
import 'package:birimcevirici/ozellikler/cevirici/alan/cevir.dart';
import 'package:birimcevirici/ozellikler/cevirici/sunum/cevirici_ekrani.dart';
import 'package:birimcevirici/ozellikler/cevirici/veri/asset_donusum_deposu.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

const _tablo = [
  BirimDonusumu(kategori: 'uzunluk', kaynak: 'km', hedef: 'm', carpan: 1000),
];

Future<void> _ac(WidgetTester tester) async {
  await tester.pumpWidget(
    MaterialApp(
      theme: uygulamaTemasi(),
      home: CeviriciEkrani(depo: AssetDonusumDeposu()),
    ),
  );
  await tester.pump(const Duration(milliseconds: 500));
}

void main() {
  test(
    'F1 cevir: 5 km → 5000 m',
    () => expect(cevir(5, 'km', 'm', _tablo), 5000),
  );
  test('F1 cevir: ters yön 2500 m → 2.5 km', () {
    expect(cevir(2500, 'm', 'km', _tablo), 2.5);
  });

  testWidgets('F1 ekran: 5 km → 5000 gösterilir', (tester) async {
    await _ac(tester);
    await tester.enterText(find.byKey(const ValueKey('cevirici.girdi')), '5');
    await tester.pump();
    expect(find.text('5000'), findsOneWidget);
  });

  testWidgets('F3 ekran: sayı olmayan girdi uyarı gösterir', (tester) async {
    await _ac(tester);
    await tester.enterText(find.byKey(const ValueKey('cevirici.girdi')), 'abc');
    await tester.pump();
    expect(find.text('Geçerli bir sayı girin'), findsOneWidget);
  });
}
