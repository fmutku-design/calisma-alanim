// ÜRETİLMİŞ DOSYA — elle düzenleme. Kaynak: tasarim.json (scripts/tasarim.py uret)
import 'package:flutter/material.dart';

abstract final class TasarimRenk {
  static const Color birincil = Color(0xFF1E6B52);
  static const Color birincilUstu = Color(0xFFFFFFFF);
  static const Color arkaplan = Color(0xFFF4F7F5);
  static const Color yuzey = Color(0xFFFFFFFF);
  static const Color metin = Color(0xFF1A1C1B);
  static const Color metinIkincil = Color(0xFF5B6360);
  static const Color hata = Color(0xFFB3261E);
}

abstract final class TasarimYazi {
  static const TextStyle baslik = TextStyle(
    fontFamily: 'Roboto',
    fontSize: 20,
    fontWeight: FontWeight.w700,
    height: 28 / 20,
    color: TasarimRenk.birincilUstu,
  );
  static const TextStyle govde = TextStyle(
    fontFamily: 'Roboto',
    fontSize: 16,
    fontWeight: FontWeight.w400,
    height: 24 / 16,
    color: TasarimRenk.metin,
  );
  static const TextStyle etiket = TextStyle(
    fontFamily: 'Roboto',
    fontSize: 14,
    fontWeight: FontWeight.w400,
    height: 20 / 14,
    color: TasarimRenk.metinIkincil,
  );
  static const TextStyle sonuc = TextStyle(
    fontFamily: 'Roboto',
    fontSize: 32,
    fontWeight: FontWeight.w700,
    height: 40 / 32,
    color: TasarimRenk.birincil,
  );
  static const TextStyle hata = TextStyle(
    fontFamily: 'Roboto',
    fontSize: 14,
    fontWeight: FontWeight.w400,
    height: 20 / 14,
    color: TasarimRenk.hata,
  );
}

abstract final class TasarimBosluk {
  static const double s8 = 8;
  static const double s16 = 16;
  static const double s24 = 24;
  static const double s32 = 32;
}

abstract final class TasarimKose {
  static const double kart = 12;
  static const double girdi = 8;
}

abstract final class TasarimBilesen {
  static const double appBarYukseklik = 56;
  static const double girdiYukseklik = 56;
  static const double sonucKartYukseklik = 120;
}
