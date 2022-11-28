from handlers.filereader import FileReader
from random import shuffle

#   Sovellustoteutuksen sisältävä luokka    #
# ----------------------------------------- #
# Annetaan viitteenä käyttöliittymälle.     #


class Flashcard:
    def __init__(self):
        # Osoite kansioon, josta tarkistetaan korttipakat automaattisesti
        self.__packfolder = "kortit"
        self.__packs = []
        self.__activepack = None

        self.__packorder = []

    # Hakee _packfolder-muuttujan osoittaman kansion .xmlpack tiedostot
    def get_files_in_folder(self):
        self.__packs = FileReader.get_files(
            self.__packfolder, ".xmlpack", True)
        return self.__packs

    # Lataa tietyn korttipakan tiedot valmiiksi käsittelyä varten
    def load_pack(self, path):
        self.__activepack = FileReader.load_from_xml(path)
        self.generate_pack_linear_order()
        return self.__activepack is not None

    # Järjestää kortit normaaliin järjestykseensä
    def generate_pack_linear_order(self):
        self.__packorder = [i for i in range(len(self.__activepack))]

    # Järjestää kortit satunnaiseen järjestykseen
    def generate_pack_random_order(self):
        self.generate_pack_linear_order()
        shuffle(self.__packorder)

    # Palauttaa korttien lauseet samassa järjestyksessä kuin pack.__cards
    def get_sentences(self):
        if self.__activepack is None:
            return []
        return [self.__activepack.get_card(i).sentence for i in range(len(self.__activepack))]

    # Palauttaa pakan seuraavan kortin, ja nostattaa __nextcard-muuttujaa yhdellä
    def get_next_card(self):
        if self.__activepack is None or len(self.__packorder) == 0:
            return None
        card = self.__activepack.get_card(self.__packorder.pop(-1))
        return card

    # Palauttaa pakan tiedoston nimen
    def get_pack_filename(self):
        if self.__activepack is None:
            return None
        return self.__activepack.path

    @property
    def file_error(self):
        return FileReader.lasterror

    @property
    def packfolder(self):
        return self.__packfolder


    # -- Korttien set/get metodit --
    def get_card_sentence(self, index):
        if self.__activepack is not None:
            return self.__activepack.get_card(index).sentence

    def set_card_sentence(self, index, value):
        if self.__activepack is not None:
            self.__activepack.get_card(index).sentence = value

    def get_card_reading(self, index):
        if self.__activepack is not None:
            return self.__activepack.get_card(index).reading

    def set_card_reading(self, index, value):
        if self.__activepack is not None:
            self.__activepack.get_card(index).reading = value

    def get_card_translation(self, index):
        if self.__activepack is not None:
            return self.__activepack.get_card(index).translation

    def set_card_translation(self, index, value):
        if self.__activepack is not None:
            self.__activepack.get_card(index).translation = value

    

    
