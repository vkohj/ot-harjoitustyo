from data.pack import Pack
from data.card import Card
import unittest


class TestPack(unittest.TestCase):
    def setUp(self):
        card1 = Card("こちらは**例文**です", "れいぶん", "esimerkkilause")
        card2 = Card("私は**車**です", "くるま", "auto")

        self.pack = Pack("Esimerkkipakka", "pack.xmlpack")
        self.pack.add_card(card1)
        self.pack.add_card(card2)

    def test_get_card_returns_none_on_invalid_index(self):
        self.assertEqual(self.pack.get_card(99), None)
        self.assertEqual(self.pack.get_card(-9), None)

    def test_unsaved_changes_is_false_by_default(self):
        self.assertEqual(self.pack.unsaved_changes, False)

    def test_unsaved_changes_can_be_changed(self):
        self.pack.unsaved_changes = True
        self.assertEqual(self.pack.unsaved_changes, True)
