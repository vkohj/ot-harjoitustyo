import os
import xml.etree.ElementTree as ET
from data.pack import Pack
from data.card import Card

#   Tiedostojen lukemiseen tarkoitettu luokka    #
#   -----------------------------------------    #
# Tätä luokkaa käytetään erilaisten tiedostojen  #
# ja hakemistojen lukemiseen                     #


class FileReader:

    lasterror = ""

    # Palauttaa tiedostot, jotka päättyvät tiettyyn merkkijonoon
    # kansio luodaan, jos sitä ei ole ja "create" on tosi
    @staticmethod
    def get_files(path, suffix="", create=False):

        if not os.path.exists(path):
            if create:
                os.makedirs(path)
            else:
                return []

        files = os.listdir(path)
        if suffix != "":
            files = [f for f in files if f.endswith(suffix)]

        return files

    # Lataa .xmlpack tiedosto
    @staticmethod
    def load_from_xml(path):
        if not os.path.exists(path):
            FileReader.lasterror = "Tiedostoa ei löytynyt"
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
        
        # TODO: Siirtyminen pois yleisestä Exception-luokasta
        except Exception as ex:
            FileReader.lasterror = "Virhe lukiessa XML-tiedostoa\n" + str(ex)
            return None

        return pack

    # Tallenna .xmlpack tiedosto
    # Funktio käyttää Pack.path muuttujaa osoitteena.
    # TODO: Tulevaisuudessa osoitteen voisi antaa itse, ja se tarkistettaisiin virheistä
    @staticmethod
    def save_to_xml(pack):
        if not os.path.exists(pack.path):
            FileReader.lasterror = "Tiedostoa ei löytynyt"
            return False

        try:
            

        # TODO: Siirtyminen pois yleisestä Exception-luokasta
        except Exception as ex:
            FileReader.lasterror = "Virhe kirjoittaessa XML-tiedostoa\n" + str(ex)
            return None

        return pack
        
        
