from handlers.filereader import FileReader

#   Sovellustoteutuksen sisältävä luokka    #
# ----------------------------------------- #
# Annetaan viitteenä käyttöliittymälle.     #

class Flashcard:
    def __init__(self):
        # Osoite kansioon, josta tarkistetaan korttipakat automaattisesti
        self.__packfolder = "kortit"
        self.__packs = []
        self.__activepack = None

        self.__nextcard = 0

    # Hakee _packfolder-muuttujan osoittaman kansion .xmlpack tiedostot
    def get_files_in_folder(self):
        self.__packs = FileReader.get_files(self.__packfolder, ".xmlpack", True)
        return self.__packs

    # Lataa tietyn korttipakan tiedot valmiiksi käsittelyä varten
    def load_pack(self, path):
        self.__activepack = FileReader.load_from_xml(path)
        self.__nextcard = 0
        return self.__activepack is not None

    # Palauttaa pakan seuraavan kortin, ja nostattaa __nextcard-muuttujaa yhdellä
    def get_next_card(self):
        if self.__activepack is None:
            return None
        card = self.__activepack.get_card(self.__nextcard)
        self.__nextcard += 1
        return card

    @property
    def file_error(self):
        return FileReader.lasterror

    @property
    def packfolder(self):
        return self.__packfolder
