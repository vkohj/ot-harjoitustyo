import unittest
import os
import xml.etree.ElementTree as ET
import pytest  # pylint: disable=import-error
from data.pack import Pack
from data.card import Card
from handlers.filereader import FileReader


class TestFileReader(unittest.TestCase):
    def setUp(self):
        FileReader.lasterror = ""

    @pytest.fixture
    def use_tempdir(self, tmp_path, monkeypatch):
        # change to pytest-provided temporary directory
        monkeypatch.chdir(tmp_path)

    @pytest.fixture
    def create_test_files(self):
        os.mkdir("get_files_test")
        open("get_files_test/a.txt", 'w').close()
        open("get_files_test/ba.xmlpack", 'w').close()
        open("get_files_test/fo.xmlpack", 'w').close()
        open("get_files_test/999.xmlpack", 'w').close()

    @pytest.mark.usefixtures("use_tempdir")
    def test_get_files_empty_path_returns_empty(self):
        val = FileReader.get_files("fake/")
        self.assertEqual(val, [])

    @pytest.mark.usefixtures("use_tempdir", "create_test_files")
    def test_get_files_returns_files_with_prefix(self):
        val = FileReader.get_files("get_files_test", ".xmlpack")
        self.assertEqual(set(val), set(
            ["ba.xmlpack", "fo.xmlpack", "999.xmlpack"]))

    @pytest.mark.usefixtures("use_tempdir", "create_test_files")
    def test_get_files_returns_all(self):
        val = FileReader.get_files("get_files_test")
        self.assertEqual(set(val), set(
            ["a.txt", "ba.xmlpack", "fo.xmlpack", "999.xmlpack"]))

    @pytest.mark.usefixtures("use_tempdir")
    def test_get_files_creates_folder(self):
        path = "unexisting_folder/folder2"
        self.assertEqual(os.path.exists(path), False)
        FileReader.get_files(path, "", True)
        self.assertEqual(os.path.exists(path), True)

    @pytest.mark.usefixtures("use_tempdir")
    def test_load_with_empty_path_returns_none(self):
        val = FileReader.load_from_xml("fake/file.xmlpack")
        self.assertEqual(val, None)

    def test_load_no_name_returns_none(self):
        val = FileReader.load_from_xml("src/tests/test_files/noname.xmlpack")
        self.assertEqual(val, None)

    def test_load_no_cards_returns_pack(self):
        val = FileReader.load_from_xml("src/tests/test_files/nocards.xmlpack")
        self.assertNotEqual(val, None)
        self.assertEqual(FileReader.lasterror, "")

    def test_load_corrupted_returns_none(self):
        val = FileReader.load_from_xml(
            "src/tests/test_files/corrupted.xmlpack")
        self.assertEqual(val, None)
        self.assertNotEqual(FileReader.lasterror, "")

    @pytest.mark.usefixtures("use_tempdir")
    def test_load_valid_xml_returns_valid_result(self):
        pack = ET.Element("pack")
        name = ET.SubElement(pack, "name").text = "Testipakka"
        cards = ET.SubElement(pack, "cards")

        # Tarkistettavat muuttujat
        sentence = "これは**例文**です"
        reading = "れいぶん"
        translation = "esimerkkilause"

        card1 = ET.SubElement(cards, "card")
        ET.SubElement(card1, "sentence").text = sentence
        ET.SubElement(card1, "reading").text = reading
        ET.SubElement(card1, "translation").text = translation

        tree = ET.ElementTree(pack)
        tree.write("testpack.xmlpack")

        val = FileReader.load_from_xml("testpack.xmlpack")
        self.assertNotEqual(val, None)
        self.assertEqual(val.path, "testpack.xmlpack")

        # Tarkistetaan kortin 1 sisältö
        card = val.get_card(0)
        self.assertEqual(card.sentence, sentence)
        self.assertEqual(card.reading, reading)
        self.assertEqual(card.translation, translation)

    @pytest.mark.usefixtures("use_tempdir")
    def test_save_to_xml_produces_valid_xml(self):
        path = "folder/testpack.xml"
        name = "Testipakka"
        pack = Pack(name, path)

        cardlist = [["これは**例文**です", "れいぶん", "esimerkkilause"],
                    ["私は猫です", "**ねこ**", "kissa"]]
        for i in range(2):
            cardlist.append(
                Card(cardlist[i][0], cardlist[i][1], cardlist[i][2]))

        card1 = Card(cardlist[0][0], cardlist[0][1], cardlist[0][2])
        card2 = Card(cardlist[1][0], cardlist[1][1], cardlist[1][2])

        pack.add_card(card1)
        pack.add_card(card2)

        val = FileReader.save_to_xml(pack)
        self.assertEqual(FileReader.lasterror, "")
        self.assertEqual(val, True)
        self.assertEqual(os.path.exists(path), True)

        # Pakan tiedot ovat oikein
        tree = ET.parse(path)
        root = tree.getroot()

        self.assertEqual(root.find('name').text, name)
        i = 0
        for card in root.findall('cards/card'):
            self.assertEqual(card.find('sentence').text, cardlist[i][0])
            self.assertEqual(card.find('reading').text, cardlist[i][1])
            self.assertEqual(card.find('translation').text, cardlist[i][2])
            i += 1
