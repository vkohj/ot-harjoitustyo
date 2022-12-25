import os
import xml.etree.ElementTree as ET
from data.pack import Pack
from data.card import Card

class FileReader:
    """Tiedostojen lukemiseen ja tallentamiseen tarkoitettu luokka

    Attributes:
        lasterror: Viimeisin virheviesti lukiessa/tallentaessa tiedostoa
    """

    lasterror = ""

    # Palauttaa tiedostot, jotka päättyvät tiettyyn merkkijonoon
    # kansio luodaan, jos sitä ei ole ja "create" on tosi
    @staticmethod
    def get_files(path, suffix="", create=False):
        """Palauttaa tiedostot, jotka päättyvät tiettyyn merkkijonoon

        Args:
            path (_type_): Kansion osoite.
            suffix (str, optional): Palauta ainoastaan tiedostot, joiden
            nimi päättyy tähän. Defaults to "".
            create (bool, optional): Luo kansio, jos tosi ja kansiota ei löydy. Defaults to False.

        Returns:
            list: Tiedostojen nimet, jotka täyttävät annetut argumentit.
        """

        if not os.path.exists(path):
            if create:
                os.makedirs(path)
            else:
                return []

        files = os.listdir(path)
        if suffix != "":
            files = [f for f in files if f.endswith(suffix)]

        return files

    @staticmethod
    def load_from_xml(path):
        """Lataa .xmlpack-tiedosto Pack-luokkaan.

        Args:
            path (string): Tiedoston osoite.

        Returns:
            Pack: Luotu korttipakka.
            None: Virhe lukiessa tiedostoa.
        """

        if not os.path.exists(path):
            FileReader.lasterror = f'Tiedostoa "{path}" ei löytynyt'
            return None

        try:
            tree = ET.parse(path)
            root = tree.getroot()

            # Korttipakan tiedot
            p_name = root.find('name')
            if p_name is None:
                FileReader.lasterror = "Korruptoitunut korttipakka: pakalta puuttuu <name>"
                return None
            pack = Pack(p_name.text, path)

            # Lue kortit ja lisää ne pakkaan
            for card in root.iter('card'):
                p_sentence = card.find('sentence')
                p_reading = card.find('reading')
                p_translation = card.find('translation')
                pack.add_card(
                    Card(p_sentence.text, p_reading.text, p_translation.text))


        except ET.ParseError as ex:
            FileReader.lasterror = f'Virhe lukiessa tiedostoa "{path}]"\n' + str(
                ex)
            return None

        except PermissionError:
            FileReader.lasterror = "Tiedostohallintaan liittyviä oikeuksia puuttuu."
            return False

        return pack


    @staticmethod
    def save_to_xml(pack):
        """Tallenna korttipakka .xmlpack-tiedostoon.

        Args:
            pack (Pack): Korttipakka-objekti.

        Returns:
            boolean: Tosi, jos tallennus onnistui, muuten epätosi.
        """

        # TODO: Kauniimman xml-tiedoston tuottaminen
        # Vasta Python 3.9 valitettavasti tarjoaa indent() komennon
        # https://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python

        path = pack.path.split("/")
        folder = "./" + "/".join(path[:len(path)-1])
        if not os.path.exists(folder):
            os.makedirs(folder)

        try:
            xmlpack = ET.Element("pack")
            ET.SubElement(xmlpack, "name").text = pack.name
            cards = ET.SubElement(xmlpack, "cards")

            for i in range(len(pack)):
                card = pack.get_card(i)

                xmlcard = ET.SubElement(cards, "card")
                ET.SubElement(xmlcard, "sentence").text = card.sentence
                ET.SubElement(xmlcard, "reading").text = card.reading
                ET.SubElement(xmlcard, "translation").text = card.translation

            tree = ET.ElementTree(xmlpack)
            tree.write(pack.path, "UTF-8")

        except ET.ParseError as ex:
            FileReader.lasterror = "Virhe kirjoittaessa XML-tiedostoa\n" + \
                str(ex)
            return False

        except PermissionError:
            FileReader.lasterror = "Tiedostohallintaan liittyviä oikeuksia puuttuu."
            return False

        return True


    @staticmethod
    def load_to_dict(path):
        """Lataa kaikki xml-tiedoston elementit sanakirjaan.

        Args:
            path (string): Tiedoston osoite.

        Returns:
            dict: Sanakirja, sisältäen elementin ja sen tekstin.
            None: Luku epäonnistui.
        """

        if not os.path.exists(path):
            FileReader.lasterror = f'Tiedostoa "{path}" ei löytynyt'
            return None

        dictionary = {}

        try:
            tree = ET.parse(path)

            i = 0
            for element in tree.iter():
                i += 1

                name = element.find('name')
                value = element.find('value')
                if name is None or value is None:
                    FileReader.lasterror = f"""Jätetään pois asetus indeksissä [{i}]
                     palautettavasta listasta. Tiedosto: "{path}"."""
                    continue

                name = name.text
                value = value.text

                if name in dictionary:
                    FileReader.lasterror = f"""Avain "{name}" löytyy jo listasta
                     ({dict[name]} -> {value}). Tiedosto: "{path}"."""

                dictionary[name] = value

        except ET.ParseError as ex:
            FileReader.lasterror = f'Virhe lukiessa tiedostoa "{path}]"\n' + str(
                ex)
            return None

        except PermissionError:
            FileReader.lasterror = "Tiedostohallintaan liittyviä oikeuksia puuttuu."
            return False

        return dictionary


    @staticmethod
    def save_dict_to_file(dictionary, file_path):
        """Tallenna sanakirjan .xml-tiedostoon, jossa sanakirjan avain on elementin
        nimi ja avaimen sisältö elementin teksti.

        Args:
            dictionary (dict): Tallennettava sanakirja.
            file_path (string): Tiedoston osoite.

        Returns:
            boolean: Tosi, jos tallennus onnistui, muuten epätosi.
        """

        path = file_path.split("/")
        folder = "./" + "/".join(path[:len(path)-1])
        if not os.path.exists(folder):
            os.makedirs(folder)

        try:
            xmlpack = ET.Element("data")

            for key, value in dictionary.items():
                item = ET.SubElement(xmlpack, "item")
                ET.SubElement(item, "name").text = key
                ET.SubElement(item, "value").text = value

            tree = ET.ElementTree(xmlpack)
            tree.write(file_path, "UTF-8")

        except ET.ParseError as ex:
            FileReader.lasterror = "Virhe kirjoittaessa XML-tiedostoa\n" + \
                str(ex)
            return False

        except PermissionError:
            FileReader.lasterror = "Tiedostohallintaan liittyviä oikeuksia puuttuu."
            return False

        return True
