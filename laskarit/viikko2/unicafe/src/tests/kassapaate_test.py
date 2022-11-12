import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassa = Kassapaate()
        self.kortti = Maksukortti(10000)

    def test_luodun_kassapaatteen_raha(self):
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)

    def test_luonnissa_lounaita_ei_ole_myyty(self):
        self.assertEqual(self.kassa.maukkaat, 0)
        self.assertEqual(self.kassa.edulliset, 0)

    def test_edullinen_kateismaksu_riittava(self):
        vaihtoraha = self.kassa.syo_edullisesti_kateisella(250)
        self.assertEqual(self.kassa.edulliset, 1)
        self.assertEqual(self.kassa.kassassa_rahaa, 100240)
        self.assertEqual(vaihtoraha, 10)

    def test_maukkaat_kateismaksu_riittava(self):
        vaihtoraha = self.kassa.syo_maukkaasti_kateisella(410)
        self.assertEqual(self.kassa.maukkaat, 1)
        self.assertEqual(self.kassa.kassassa_rahaa, 100400)
        self.assertEqual(vaihtoraha, 10)

    def test_edullinen_kateismaksu_eiriita(self):
        vaihtoraha = self.kassa.syo_edullisesti_kateisella(200)
        self.assertEqual(self.kassa.edulliset, 0)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)
        self.assertEqual(vaihtoraha, 200)

    def test_maukkaat_kateismaksu_eiriita(self):
        vaihtoraha = self.kassa.syo_maukkaasti_kateisella(200)
        self.assertEqual(self.kassa.maukkaat, 0)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)
        self.assertEqual(vaihtoraha, 200)

    def test_edullinen_korttimaksu_riittava(self):
        totuus = self.kassa.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(self.kassa.edulliset, 1)
        self.assertEqual(self.kortti.saldo, 9760)
        self.assertEqual(totuus, True)

    def test_maukkaat_korttimaksu_riittava(self):
        totuus = self.kassa.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(self.kassa.maukkaat, 1)
        self.assertEqual(self.kortti.saldo, 9600)
        self.assertEqual(totuus, True)

    def test_edullinen_korttimaksu_eiriita(self):
        kortti = Maksukortti(200)
        totuus = self.kassa.syo_edullisesti_kortilla(kortti)
        self.assertEqual(self.kassa.edulliset, 0)
        self.assertEqual(kortti.saldo, 200)
        self.assertEqual(totuus, False)

    def test_maukkaat_korttimaksu_eiriita(self):
        kortti = Maksukortti(200)
        totuus = self.kassa.syo_maukkaasti_kortilla(kortti)
        self.assertEqual(self.kassa.maukkaat, 0)
        self.assertEqual(kortti.saldo, 200)
        self.assertEqual(totuus, False)

    def test_kassan_saldo_ei_muutu_kortilla(self):
        self.kassa.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)

    def test_saldot_nousevat_ladatessa_korttia(self):
        self.kassa.lataa_rahaa_kortille(self.kortti, 100)
        self.assertEqual(self.kortti.saldo, 10100)
        self.assertEqual(self.kassa.kassassa_rahaa, 100100)    

    def test_latauksessa_saldot_ei_muutu_jos_negatiivinen(self):
        self.kassa.lataa_rahaa_kortille(self.kortti, -100)
        self.assertEqual(self.kortti.saldo, 10000)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)    

    
