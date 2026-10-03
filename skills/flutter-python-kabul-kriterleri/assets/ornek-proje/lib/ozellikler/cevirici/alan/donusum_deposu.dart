import 'birim_donusumu.dart';

/// Alan katmanının veri sözleşmesi. Veri katmanı bunu uygular; sunum yalnızca bunu bilir.
abstract interface class DonusumDeposu {
  Future<List<BirimDonusumu>> hepsi();
}
