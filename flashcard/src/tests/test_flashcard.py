import os
import unittest
import pytest  # pylint: disable=import-error

from flashcard import Flashcard
from data.pack import Pack

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
