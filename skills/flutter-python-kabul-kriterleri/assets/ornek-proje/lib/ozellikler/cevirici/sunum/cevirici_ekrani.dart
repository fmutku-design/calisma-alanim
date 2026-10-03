import 'package:flutter/material.dart';

import '../../../cekirdek/tema/tasarim.g.dart';
import '../alan/birim_donusumu.dart';
import '../alan/cevir.dart';
import '../alan/donusum_deposu.dart';
import 'sonuc_karti.dart';

class CeviriciEkrani extends StatefulWidget {
  const CeviriciEkrani({super.key, required this.depo});

  final DonusumDeposu depo;

  @override
  State<CeviriciEkrani> createState() => _CeviriciEkraniDurumu();
}

class _CeviriciEkraniDurumu extends State<CeviriciEkrani> {
  List<BirimDonusumu> _tablo = const [];
  String _girdi = '';
  String? _kaynak;
  String? _hedef;

  @override
  void initState() {
    super.initState();
    widget.depo.hepsi().then((tablo) {
      if (!mounted) return;
      setState(() {
        _tablo = tablo;
        _kaynak = tablo.first.kaynak;
        _hedef = tablo.first.hedef;
      });
    });
  }

  List<String> get _kaynaklar => {
    for (final d in _tablo) ...[d.kaynak, d.hedef],
  }.toList();

  String get _sonucMetni {
    final deger = double.tryParse(_girdi);
    if (_girdi.isEmpty || _kaynak == null || _hedef == null) return '';
    if (deger == null) return 'Geçerli bir sayı girin';
    final sonuc = cevir(deger, _kaynak!, _hedef!, _tablo);
    if (sonuc == null) return '';
    return sonuc == sonuc.roundToDouble()
        ? sonuc.toInt().toString()
        : sonuc.toString();
  }

  Widget _secici(
    Key key,
    String? deger,
    List<String> secenekler,
    ValueChanged<String?> degisti,
  ) {
    return Expanded(
      child: DropdownButtonFormField<String>(
        key: key,
        initialValue: deger,
        items: [
          for (final s in secenekler)
            DropdownMenuItem(value: s, child: Text(s)),
        ],
        onChanged: degisti,
      ),
    );
  }

  Widget _birimSatiri() {
    final hedefSecenekleri = _kaynak == null
        ? <String>[]
        : hedefler(_kaynak!, _tablo);
    return Row(
      children: [
        _secici(
          const ValueKey('cevirici.kaynakBirim'),
          _kaynak,
          _kaynaklar,
          (v) => setState(() {
            _kaynak = v;
            _hedef = hedefler(v!, _tablo).first;
          }),
        ),
        const SizedBox(width: TasarimBosluk.s16),
        _secici(
          const ValueKey('cevirici.hedefBirim'),
          _hedef,
          hedefSecenekleri,
          (v) => setState(() => _hedef = v),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    final sonuc = _sonucMetni;
    return Scaffold(
      appBar: AppBar(
        key: const ValueKey('cevirici.baslik'),
        title: const Text('Birim Çevirici'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(TasarimBosluk.s16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const SizedBox(height: TasarimBosluk.s8),
            SizedBox(
              height: TasarimBilesen.girdiYukseklik,
              child: TextField(
                key: const ValueKey('cevirici.girdi'),
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(labelText: 'Değer'),
                onChanged: (v) => setState(() => _girdi = v),
              ),
            ),
            const SizedBox(height: TasarimBosluk.s16),
            _birimSatiri(),
            const SizedBox(height: TasarimBosluk.s32),
            SonucKarti(
              key: const ValueKey('cevirici.sonucKarti'),
              metin: sonuc,
              hata: sonuc == 'Geçerli bir sayı girin',
            ),
          ],
        ),
      ),
    );
  }
}
