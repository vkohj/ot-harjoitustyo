import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_luodun_kortin_saldo_on_oikein(self):
        self.assertEqual(self.maksukortti.saldo, 1000)

    def test_rahan_lataaminen_kasvattaa_saldoa(self):
        self.maksukortti.lataa_rahaa(1000)
        self.assertEqual(self.maksukortti.saldo, 2000)

    def test_saldo_vahenee_jos_rahaa(self):
        self.maksukortti.ota_rahaa(500)
        self.assertEqual(self.maksukortti.saldo, 500)

    def test_saldo_ei_muutu_jos_rahaton(self):
        self.maksukortti.ota_rahaa(1500)
        self.assertEqual(self.maksukortti.saldo, 1000)

    def test_metodi_palauttaa_epatosi_jos_ei_saldoa(self):
        self.assertEqual(self.maksukortti.ota_rahaa(1500), False)

    def test_metodi_palauttaa_tosi_jos_saldoa(self):
        self.assertEqual(self.maksukortti.ota_rahaa(500), True)

    def test_saldo_euroissa_tulostaa_oikein(self):
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")
    
