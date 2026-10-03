import 'package:flutter/material.dart';

import 'cekirdek/tema/tema.dart';
import 'ozellikler/cevirici/sunum/cevirici_ekrani.dart';
import 'ozellikler/cevirici/veri/asset_donusum_deposu.dart';

class Uygulama extends StatelessWidget {
  const Uygulama({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Birim Çevirici',
      debugShowCheckedModeBanner: false,
      theme: uygulamaTemasi(),
      home: CeviriciEkrani(depo: AssetDonusumDeposu()),
    );
  }
}
