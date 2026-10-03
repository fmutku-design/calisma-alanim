import 'package:flutter/material.dart';

import '../../../cekirdek/tema/tasarim.g.dart';

class SonucKarti extends StatelessWidget {
  const SonucKarti({super.key, required this.metin, required this.hata});

  final String metin;
  final bool hata;

  @override
  Widget build(BuildContext context) {
    return Container(
      height: TasarimBilesen.sonucKartYukseklik,
      alignment: Alignment.center,
      decoration: BoxDecoration(
        color: TasarimRenk.yuzey,
        borderRadius: BorderRadius.circular(TasarimKose.kart),
      ),
      child: Text(metin, style: hata ? TasarimYazi.hata : TasarimYazi.sonuc),
    );
  }
}
