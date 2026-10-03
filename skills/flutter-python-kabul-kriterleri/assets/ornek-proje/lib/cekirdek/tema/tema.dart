import 'package:flutter/material.dart';

import 'tasarim.g.dart';

/// Tasarım sabitlerini (tasarim.g.dart) Material temasına bağlar.
/// Bu dosyada da yalnızca Tasarim* sabitleri kullanılır; sayı veya renk kodu yazılmaz.
ThemeData uygulamaTemasi() {
  final girdiKenari = OutlineInputBorder(
    borderRadius: BorderRadius.circular(TasarimKose.girdi),
  );
  return ThemeData(
    useMaterial3: true,
    fontFamily: 'Roboto',
    scaffoldBackgroundColor: TasarimRenk.arkaplan,
    colorScheme: ColorScheme.fromSeed(
      seedColor: TasarimRenk.birincil,
      primary: TasarimRenk.birincil,
      onPrimary: TasarimRenk.birincilUstu,
      surface: TasarimRenk.yuzey,
      onSurface: TasarimRenk.metin,
      error: TasarimRenk.hata,
    ),
    appBarTheme: const AppBarTheme(
      backgroundColor: TasarimRenk.birincil,
      foregroundColor: TasarimRenk.birincilUstu,
      toolbarHeight: TasarimBilesen.appBarYukseklik,
      titleTextStyle: TasarimYazi.baslik,
    ),
    inputDecorationTheme: InputDecorationTheme(
      border: girdiKenari,
      labelStyle: TasarimYazi.etiket,
    ),
    textTheme: const TextTheme(bodyLarge: TasarimYazi.govde),
  );
}
