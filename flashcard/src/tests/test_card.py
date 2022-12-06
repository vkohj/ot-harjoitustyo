from data.card import Card
import unittest


class TestCard(unittest.TestCase):
    def setUp(self):
        self.card = Card("こちらは**例文**です", "れいぶん", "esimerkkilause")

    def test_card_get_returns_correct_info(self):
        self.assertEqual(self.card.sentence, "こちらは**例文**です")
        self.assertEqual(self.card.reading, "れいぶん")
        self.assertEqual(self.card.translation, "esimerkkilause")

    def test_card_get_returns_new_correct_info(self):
        self.card.sentence = "**新しい**例文"
        self.card.reading = "あたらしい"
        self.card.translation = "uusi"

        self.assertEqual(self.card.sentence, "**新しい**例文")
        self.assertEqual(self.card.reading, "あたらしい")
        self.assertEqual(self.card.translation, "uusi")

    def test_card_set_does_not_allow_empty_value(self):
        self.card.sentence = ""
        self.card.reading = ""
        self.card.translation = ""
        self.assertEqual(self.card.sentence, "こちらは**例文**です")
        self.assertEqual(self.card.reading, "れいぶん")
        self.assertEqual(self.card.translation, "esimerkkilause")
