import os
import unittest
import pytest  # pylint: disable=import-error

from flashcard import Flashcard
from data.card import Card


class TestFlashcard(unittest.TestCase):
    def setUp(self):
        self.flashcard = Flashcard()

    @pytest.fixture
    def use_tempdir(self, tmp_path, monkeypatch):
        # change to pytest-provided temporary directory
        monkeypatch.chdir(tmp_path)

    @pytest.mark.usefixtures("use_tempdir")
    def test_get_folders_gets_packfiles(self):
        os.mkdir("kortit")
        open("kortit/a.txt", 'w').close()
        open("kortit/ba.xmlpack", 'w').close()
        open("kortit/fo.xmlpack", 'w').close()

        cards = set(self.flashcard.get_files_in_folder())
        self.assertEqual(cards, {"ba.xmlpack", "fo.xmlpack"})

    @pytest.mark.usefixtures("use_tempdir")
    def test_get_folders_returns_none(self):
        open("a.xmlpack", 'w').close()

        cards = self.flashcard.get_files_in_folder()
        self.assertEqual(len(cards), 0)

    def test_load_pack_returns_pack(self):
        val = self.flashcard.load_pack(
            "src/tests/test_files/working.xmlpack")
        self.assertTrue(val)

    def test_load_pack_returns_none_on_corrupt(self):
        val = self.flashcard.load_pack(
            "src/tests/test_files/corrupted.xmlpack")
        self.assertEqual(val, False)

    @pytest.mark.usefixtures("use_tempdir")
    def test_load_pack_returns_none_if_doesnt_exist(self):
        val = self.flashcard.load_pack(
            "rariro.xmlpack")
        self.assertEqual(val, False)

    def test_generate_pack_linear_order_checks_if_pack_exists(self):
        self.flashcard.generate_pack_linear_order()

    def test_generate_pack_random_order_checks_if_pack_exists(self):
        self.flashcard.generate_pack_random_order()

    def test_get_sentences_returns_all_sentences(self):
        self.flashcard.load_pack(
            "src/tests/test_files/working.xmlpack")

        val = self.flashcard.get_sentences()
        self.assertEqual(set(val), {"この**文**はテストです。", "アプリを**検索**"})
    
    def test_get_sentences_returns_empty_list_when_no_cards(self):
        self.flashcard.load_pack(
            "src/tests/test_files/nocards.xmlpack")
        val = self.flashcard.get_sentences()
        self.assertEqual(len(val), 0)

    def test_save_pack_returns_false_when_no_pack(self):
        self.assertFalse(self.flashcard.save_pack())

    def test_get_pack_name_returns_name(self):
        self.flashcard.load_pack(
            "src/tests/test_files/working.xmlpack")

        self.assertEqual(self.flashcard.get_pack_name(), "Testipakka")

    def test_next_card_returns_none_when_no_pack(self):
        self.assertEqual(self.flashcard.get_next_card(), None)

    def test_next_card_returns_none_when_no_cards_remaining(self):
        self.flashcard.load_pack(
            "src/tests/test_files/nocards.xmlpack")
        self.assertEqual(self.flashcard.get_next_card(), None)

    def test_next_card_returns_card(self):
        self.flashcard.load_pack(
            "src/tests/test_files/working.xmlpack")
        card = self.flashcard.get_next_card()
        self.assertTrue(isinstance(card, Card))

    def test_get_pack_filename_returns_filename(self):
        self.flashcard.load_pack(
            "src/tests/test_files/working.xmlpack")

        self.assertEqual(self.flashcard.get_pack_filename(), "src/tests/test_files/working.xmlpack")

    def test_get_pack_filename_returns_none_when_no_pack(self):
        self.assertEqual(self.flashcard.get_pack_filename(), None)

    def test_get_pack_changed_returns_changes(self):
        self.flashcard.load_pack(
            "src/tests/test_files/working.xmlpack")

        self.assertFalse(self.flashcard.get_pack_changed())
        self.flashcard.set_card_sentence(0, "a**a**a")
        self.assertTrue(self.flashcard.get_pack_changed())

    def test_get_pack_changed_returns_false_on_empty(self):
        self.assertFalse(self.flashcard.get_pack_changed())
