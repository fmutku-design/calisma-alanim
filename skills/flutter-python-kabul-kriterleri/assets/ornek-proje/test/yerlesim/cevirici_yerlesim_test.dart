// ÜRETİLMİŞ DOSYA — elle düzenleme. Kaynak: ekranlar.json (scripts/tasarim.py uret)
import 'package:birimcevirici/cekirdek/tema/tema.dart';
import 'package:birimcevirici/ozellikler/cevirici/sunum/cevirici_ekrani.dart';
import 'package:birimcevirici/ozellikler/cevirici/veri/asset_donusum_deposu.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import '../yardimci/tasarim_fontlari.dart';

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

  testWidgets('T4 cevirici: cevirici.baslik adet 1', (tester) async {
    await ac(tester);
    expect(find.byKey(const ValueKey('cevirici.baslik')), findsNWidgets(1));
  });
  testWidgets('T4 cevirici: cevirici.baslik yukseklik 56±1 dp', (tester) async {
    await ac(tester);
    final r = tester.getRect(
      find.byKey(const ValueKey('cevirici.baslik')).first,
    );
    expect(r.height, closeTo(56, 1));
  });
  testWidgets('T4 cevirici: cevirici.baslik genislik 360±1 dp', (tester) async {
    await ac(tester);
    final r = tester.getRect(
      find.byKey(const ValueKey('cevirici.baslik')).first,
    );
    expect(r.width, closeTo(360, 1));
  });
  testWidgets('T4 cevirici: cevirici.baslik ust 0±1 dp', (tester) async {
    await ac(tester);
    final r = tester.getRect(
      find.byKey(const ValueKey('cevirici.baslik')).first,
    );
    expect(r.top, closeTo(0, 1));
  });
  testWidgets('T4 cevirici: cevirici.baslik sol 0±1 dp', (tester) async {
    await ac(tester);
    final r = tester.getRect(
      find.byKey(const ValueKey('cevirici.baslik')).first,
    );
    expect(r.left, closeTo(0, 1));
  });
  testWidgets('T4 cevirici: cevirici.girdi adet 1', (tester) async {
    await ac(tester);
    expect(find.byKey(const ValueKey('cevirici.girdi')), findsNWidgets(1));
  });
  testWidgets('T4 cevirici: cevirici.girdi yukseklik 56±1 dp', (tester) async {
    await ac(tester);
    final r = tester.getRect(
      find.byKey(const ValueKey('cevirici.girdi')).first,
    );
    expect(r.height, closeTo(56, 1));
  });
  testWidgets('T4 cevirici: cevirici.girdi genislik 328±1 dp', (tester) async {
    await ac(tester);
    final r = tester.getRect(
      find.byKey(const ValueKey('cevirici.girdi')).first,
    );
    expect(r.width, closeTo(328, 1));
  });
  testWidgets('T4 cevirici: cevirici.girdi ust 80±1 dp', (tester) async {
    await ac(tester);
    final r = tester.getRect(
      find.byKey(const ValueKey('cevirici.girdi')).first,
    );
    expect(r.top, closeTo(80, 1));
  });
  testWidgets('T4 cevirici: cevirici.girdi sol 16±1 dp', (tester) async {
    await ac(tester);
    final r = tester.getRect(
      find.byKey(const ValueKey('cevirici.girdi')).first,
    );
    expect(r.left, closeTo(16, 1));
  });
  testWidgets('T4 cevirici: cevirici.kaynakBirim adet 1', (tester) async {
    await ac(tester);
    expect(
      find.byKey(const ValueKey('cevirici.kaynakBirim')),
      findsNWidgets(1),
    );
  });
  testWidgets('T4 cevirici: cevirici.kaynakBirim genislik 156±1 dp', (
    tester,
  ) async {
    await ac(tester);
    final r = tester.getRect(
      find.byKey(const ValueKey('cevirici.kaynakBirim')).first,
    );
    expect(r.width, closeTo(156, 1));
  });
  testWidgets('T4 cevirici: cevirici.kaynakBirim ust 152±1 dp', (tester) async {
    await ac(tester);
    final r = tester.getRect(
      find.byKey(const ValueKey('cevirici.kaynakBirim')).first,
    );
    expect(r.top, closeTo(152, 1));
  });
  testWidgets('T4 cevirici: cevirici.kaynakBirim sol 16±1 dp', (tester) async {
    await ac(tester);
    final r = tester.getRect(
      find.byKey(const ValueKey('cevirici.kaynakBirim')).first,
    );
    expect(r.left, closeTo(16, 1));
  });
  testWidgets('T4 cevirici: cevirici.hedefBirim adet 1', (tester) async {
    await ac(tester);
    expect(find.byKey(const ValueKey('cevirici.hedefBirim')), findsNWidgets(1));
  });
  testWidgets('T4 cevirici: cevirici.hedefBirim genislik 156±1 dp', (
    tester,
  ) async {
    await ac(tester);
    final r = tester.getRect(
      find.byKey(const ValueKey('cevirici.hedefBirim')).first,
    );
    expect(r.width, closeTo(156, 1));
  });
  testWidgets('T4 cevirici: cevirici.hedefBirim ust 152±1 dp', (tester) async {
    await ac(tester);
    final r = tester.getRect(
      find.byKey(const ValueKey('cevirici.hedefBirim')).first,
    );
    expect(r.top, closeTo(152, 1));
  });
  testWidgets('T4 cevirici: cevirici.hedefBirim sol 188±1 dp', (tester) async {
    await ac(tester);
    final r = tester.getRect(
      find.byKey(const ValueKey('cevirici.hedefBirim')).first,
    );
    expect(r.left, closeTo(188, 1));
  });
  testWidgets('T4 cevirici: cevirici.sonucKarti adet 1', (tester) async {
    await ac(tester);
    expect(find.byKey(const ValueKey('cevirici.sonucKarti')), findsNWidgets(1));
  });
  testWidgets('T4 cevirici: cevirici.sonucKarti yukseklik 120±1 dp', (
    tester,
  ) async {
    await ac(tester);
    final r = tester.getRect(
      find.byKey(const ValueKey('cevirici.sonucKarti')).first,
    );
    expect(r.height, closeTo(120, 1));
  });
  testWidgets('T4 cevirici: cevirici.sonucKarti genislik 328±1 dp', (
    tester,
  ) async {
    await ac(tester);
    final r = tester.getRect(
      find.byKey(const ValueKey('cevirici.sonucKarti')).first,
    );
    expect(r.width, closeTo(328, 1));
  });
  testWidgets('T4 cevirici: cevirici.sonucKarti ust 240±1 dp', (tester) async {
    await ac(tester);
    final r = tester.getRect(
      find.byKey(const ValueKey('cevirici.sonucKarti')).first,
    );
    expect(r.top, closeTo(240, 1));
  });
  testWidgets('T4 cevirici: cevirici.sonucKarti sol 16±1 dp', (tester) async {
    await ac(tester);
    final r = tester.getRect(
      find.byKey(const ValueKey('cevirici.sonucKarti')).first,
    );
    expect(r.left, closeTo(16, 1));
  });
  testWidgets('T4 cevirici: sıra cevirici.baslik → cevirici.girdi', (
    tester,
  ) async {
    await ac(tester);
    final ust = tester.getRect(
      find.byKey(const ValueKey('cevirici.baslik')).first,
    );
    final alt = tester.getRect(
      find.byKey(const ValueKey('cevirici.girdi')).first,
    );
    expect(ust.top, lessThanOrEqualTo(alt.top));
  });
  testWidgets('T4 cevirici: sıra cevirici.girdi → cevirici.kaynakBirim', (
    tester,
  ) async {
    await ac(tester);
    final ust = tester.getRect(
      find.byKey(const ValueKey('cevirici.girdi')).first,
    );
    final alt = tester.getRect(
      find.byKey(const ValueKey('cevirici.kaynakBirim')).first,
    );
    expect(ust.top, lessThanOrEqualTo(alt.top));
  });
  testWidgets('T4 cevirici: sıra cevirici.hedefBirim → cevirici.sonucKarti', (
    tester,
  ) async {
    await ac(tester);
    final ust = tester.getRect(
      find.byKey(const ValueKey('cevirici.hedefBirim')).first,
    );
    final alt = tester.getRect(
      find.byKey(const ValueKey('cevirici.sonucKarti')).first,
    );
    expect(ust.top, lessThanOrEqualTo(alt.top));
  });
}
