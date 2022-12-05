from random import shuffle
from handlers.filereader import FileReader
from data.card import Card

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
        if self.__activepack is None:
            return False

        self.generate_pack_linear_order()
        return True

    # Tallentaa aktiivisen pakan
    def save_pack(self):
        if self.__activepack is None:
            return False
        self.__activepack.unsaved_changes = False
        return FileReader.save_to_xml(self.__activepack)

    # Järjestää kortit normaaliin järjestykseensä
    def generate_pack_linear_order(self):
        if self.__activepack:
            self.__packorder = list(range(len(self.__activepack)))

    # Järjestää kortit satunnaiseen järjestykseen
    def generate_pack_random_order(self):
        if self.__activepack:
            self.generate_pack_linear_order()
            shuffle(self.__packorder)

    def get_pack_name(self):
        if self.__activepack is None:
            raise IndexError("self.__activepack does not exist")
        return self.__activepack.name

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

    # Palauttaa onko pakkaan tehty muutoksia viime tallennuksen jälkeen
    def get_pack_changed(self):
        if self.__activepack is None:
            return False
        return self.__activepack.unsaved_changes

    @property
    def file_error(self):
        return FileReader.lasterror

    @property
    def packfolder(self):
        return self.__packfolder

    # -- Korttien set/get metodit --
    def __pack_set(self):
        if self.__activepack is None:
            return False
        self.__activepack.unsaved_changes = True
        return True

    def new_card(self, sentence, reading, translation):
        if self.__pack_set() is False:
            return False
        if sentence == "" or reading == "" or translation == "":
            return False

        card = Card(sentence, reading, translation)
        self.__activepack.add_card(card)

        return True

    def get_card_sentence(self, index):
        if self.__activepack is None:
            return None
        return self.__activepack.get_card(index).sentence

    def set_card_sentence(self, index, value):
        if self.__pack_set() is False:
            return
        self.__activepack.get_card(index).sentence = value

    def get_card_reading(self, index):
        if self.__activepack is None:
            return None
        return self.__activepack.get_card(index).reading

    def set_card_reading(self, index, value):
        if self.__pack_set() is False:
            return
        self.__activepack.get_card(index).reading = value

    def get_card_translation(self, index):
        if self.__activepack is None:
            return None
        return self.__activepack.get_card(index).translation

    def set_card_translation(self, index, value):
        if self.__pack_set() is False:
            return
        self.__activepack.get_card(index).translation = value
