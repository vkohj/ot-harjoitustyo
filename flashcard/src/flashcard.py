from random import shuffle
from handlers.filereader import FileReader
from data.card import Card


class Flashcard:
    """Sovellustoteutuksen sisältävä luokka. Annetaan viitteenä käyttöliittymälle.
    """

    def __init__(self):
        """Luokan konstruktori, luo Flashcard-sovellustoteutuksen."""

        self.__packfolder = "kortit"
        self.__packs = []
        self.__activepack = None

        self.__packorder = []
        self.__setting = {}

        self.__load_setting_file("setting.xml")

    def get_files_in_folder(self):
        """Hakee _packfolder-muuttujan osoittaman kansion .xmlpack-tiedostot

        Returns:
            list: Sisältää kaikki .xmlpack tiedostot kansiossa
        """

        self.__packs = FileReader.get_files(
            self.__packfolder, ".xmlpack", True)
        return self.__packs

    def load_pack(self, path):
        """Lataa tietyn korttipakan tiedot valmiiksi käsittelyä varten

        Args:
            path (merkkijono): Osoite korttipakkatiedostoon

        Returns:
            True, jos lataus onnistui ja pakka on nyt self.__activepack muuttujassa, muuten False.
        """

        self.__activepack = FileReader.load_from_xml(path)
        if self.__activepack is None:
            return False

        self.generate_pack_linear_order()
        return True

    def save_pack(self):
        """Tallentaa aktiivisen pakan xml-tiedostoksi. Tiedoston osoite on Pack.path.

        Returns:
            True, jos tallennus onnistui, muuten False.
        """

        if self.__activepack is None:
            return False
        self.__activepack.unsaved_changes = False
        return FileReader.save_to_xml(self.__activepack)

    def generate_pack_linear_order(self):
        """Järjestää kortit normaaliin järjestykseen,
         jotta ne voidaan sitten nostaa yksitellen Flashcard.get_next_card()-metodilla.
        """

        if self.__activepack:
            self.__packorder = list(range(len(self.__activepack)))

    def generate_pack_random_order(self):
        """Järjestää kortit satunnaiseen järjestykseen,
         jotta ne voidaan sitten nostaa yksitellen Flashcard.get_next_card()-metodilla.
        """

        if self.__activepack:
            self.generate_pack_linear_order()
            shuffle(self.__packorder)

    def get_pack_name(self):
        """Palauttaa käytössä olevan pakan nimen, joka on ladattu Flashcard.load_pack()-metodilla.

        Raises:
            IndexError: Mitään pakkaa ei ole (onnistuneesti) ladattu.

        Returns:
            string: Käytössä olevan pakan nimi
        """

        if self.__activepack is None:
            raise IndexError("self.__activepack does not exist")
        return self.__activepack.name

    def get_sentences(self):
        """Palauttaa ladatun pakan korttien lauseet.

        Returns:
            list: Korttien lauseet pack.__cards-listan järjestyksessä.
        """

        if self.__activepack is None:
            return []
        return [self.__activepack.get_card(i).sentence for i in range(len(self.__activepack))]

    def get_next_card(self):
        """Seuraten Flashcard.__packorder listaa, palauttaa seuraavan kortin
        käytössä olevasta pakasta.

        Returns:
            Card: __packorder-listan seuraavana ollut kortti.
            None: Pakkaa ei löytynyt tai siinä ei ole enää kortteja.
        """

        if self.__activepack is None or len(self.__packorder) == 0:
            return None
        card = self.__activepack.get_card(self.__packorder.pop(-1))
        return card

    def get_pack_filename(self):
        """Palauttaa käytössä olevan pakan tiedostonimen

        Returns:
            string: Pakan osoite levyllä tai verrattuna ohjelman sijaintiin
        """

        if self.__activepack is None:
            return None
        return self.__activepack.path

    def get_pack_changed(self):
        """Kertoo, onko pakan sisältöön tehty muutoksia sitten viime tallennuksen.

        Returns:
            True: Jos muutoksia on tehty, muuten False
        """

        if self.__activepack is None:
            return False
        return self.__activepack.unsaved_changes

    def __load_setting_file(self, path):
        """Lataa ohjelman asetukset .xml-tiedostosta ja lisää puuttuvat asetukset .xml-tiedostoon

        Args:
            path (string): Asetustiedoston osoite
        """

        self.__setting = FileReader.load_to_dict(path)
        changed = False
        if self.__setting is None:
            self.__setting = {}
            changed = True

        # Lisää puuttuvat asetukset tiedostoon
        changed = max(changed, self.__setting_set_if_none("font_family", ""))
        changed = max(changed, self.__setting_set_if_none("font_h1", "14"))
        changed = max(changed, self.__setting_set_if_none("font_p", "10"))
        changed = max(changed, self.__setting_set_if_none(
            "font_sentence", "12"))
        changed = max(changed, self.__setting_set_if_none(
            "font_reading", "11"))
        changed = max(changed, self.__setting_set_if_none(
            "font_translation", "11"))

        if changed:
            FileReader.save_dict_to_file(self.__setting, path)

    def __setting_set_if_none(self, key, value):
        """Lisää asetuksen sanakirjaan Flashcard.__setting, jos
        siellä ei ole jo samannimistä asetusta.

        Args:
            key (string): avain
            value (string): asetus

        Returns:
            True: Jos metodi aiheutti muutoksen, muuten False
        """

        if key not in self.__setting:
            self.__setting[key] = value
            return True
        return False

    def get_setting(self, key):
        """Julkinen funktio, joka palauttaa asetuksen Flashcard.__setting-sanakirjasta

        Args:
            key (string): avain

        Returns:
            string: asetus
            None: jos avainta ei löytynyt
        """

        if key not in self.__setting:
            return None

        return self.__setting[key]

    def set_setting(self, key, value):
        """Julkinen funktio, joka asettaa jonkin asetuksen Flashcard.__setting-sanakirjaan.

        Args:
            key (string): avain
            value (string): asetus
        """

        self.__setting[key] = value

    def save_setting(self):
        """Julkinen funktio, joka tallentaa asetukset tiedostoon setting.xml.
        """

        FileReader.save_dict_to_file(self.__setting, "setting.xml")

    @property
    def file_error(self):
        """Palauttaa staattisen FileReader-luokan viimeisimmän virheilmoituksen.

        Returns:
            string: FileReader-luokan viimeisin virheilmoitus
        """

        return FileReader.lasterror

    @property
    def packfolder(self):
        """Palauttaa kansion osoitteen, mistä Flashcard-luokka etsii .xmlpack-tiedostoja.

        Returns:
            string: osoite pakkakansioon
        """

        return self.__packfolder

    def __card_get(self, index):
        """Luokan sisäinen metodi, jolla voidaan nopeasti tarkistaa kortin kunto ennen
        kortin tietojen palauttamista.
        Tarkastaa, onko käytössä oleva pakka/kortti olemassa, ja palauttaa kortin pakasta.

        Returns:
            Card: Kortti, jos pakka ja kortti olivat olemassa.
            None: Jos pakkaa/korttia ei ollut olemassa.
        """

        if self.__activepack is None:
            return None
        card = self.__activepack.get_card(index)
        if card is None:
            return None
        return card


    def __pack_set(self, index=-1):
        """Luokan sisäinen metodi, joka ajetaan aina ennen korttien muokkaamista.
        Tarkastaa, onko käytössä oleva pakka olemassa, ja
        laittaa muutosta ilmaisevan muuttujan todeksi.

        Args:
            index (int, optional): Jos halutaan tarkastaa, onko kortti pakassa. Defaults to -1.

        Returns:
            boolean: True, jos pakka ja kortti oli olemassa ja
            Pack.unsaved_changes on muutettu todeksi, muuten False.
        """

        if self.__activepack is None:
            return False
        if index != -1 and not self.__activepack.exists(index):
            return False

        self.__activepack.unsaved_changes = True
        return True


    def new_card(self, sentence, reading, translation):
        """Lisää uuden kortin käytössä olevaan korttipakkaan.

        Args:
            sentence (string): Japaninkielinen lause
            reading (string): Lukutapa
            translation (string): Lukutavan käännös

        Returns:
            _type_: False, jos pakkaa ei ole tai jokin argumenteista oli tyhjä, muuten True
        """

        if self.__pack_set() is False:
            return False
        if sentence == "" or reading == "" or translation == "":
            return False

        card = Card(sentence, reading, translation)
        self.__activepack.add_card(card)

        return True


    def get_card_sentence(self, index):
        """Hae tämänhetkisestä korttipakasta kortin japaninkielinen lause

        Args:
            index (int): Lauseen sijainti Flashcard.get_sentences()-metodin palauttamassa listassa.

        Returns:
            string: Kortin lause.
            None: Pakkaa ei ole ladattu.
        """

        card = self.__card_get(index)
        if card is None:
            return None
        return card.sentence


    def set_card_sentence(self, index, value):
        """Aseta tämänhetkisestä korttipakasta löytyvän kortin japaninkielinen lause.

        Args:
            index (int): Lauseen sijainti Flashcard.get_sentences()-metodin palauttamassa listassa.
            value (string): Lause
        """

        if self.__pack_set(index) is False:
            return
        self.__activepack.get_card(index).sentence = value


    def get_card_reading(self, index):
        """Hae tämänhetkisestä korttipakasta kortin lauseen lukutapa

        Args:
            index (int): Lauseen sijainti Flashcard.get_sentences()-metodin palauttamassa listassa.

        Returns:
            string: Kortin lukutapa.
            None: Pakkaa ei ole ladattu.
        """

        card = self.__card_get(index)
        if card is None:
            return None
        return card.reading


    def set_card_reading(self, index, value):
        """Aseta tämänhetkisestä korttipakasta löytyvän kortin lukutapa.

        Args:
            index (int): Kortin lauseen sijainti Flashcard.get_sentences()-metodin
            palauttamassa listassa.
            value (string): Lukutapa
        """

        if self.__pack_set(index) is False:
            return
        self.__activepack.get_card(index).reading = value


    def get_card_translation(self, index):
        """Hae tämänhetkisestä korttipakasta kortin käännöslause.

        Args:
            index (int): Lauseen sijainti Flashcard.get_sentences()-metodin palauttamassa listassa.

        Returns:
            string: Kortin käännöslause.
            None: Pakkaa ei ole ladattu
        """

        card = self.__card_get(index)
        if card is None:
            return None
        return card.translation


    def set_card_translation(self, index, value):
        """Aseta tämänhetkisestä korttipakasta löytyvän kortin käännöslause.

        Args:
            index (int): Kortin lauseen sijainti
            Flashcard.get_sentences()-metodin palauttamassa listassa.
            value (string): Käännöslause
        """

        if self.__pack_set(index) is False:
            return
        self.__activepack.get_card(index).translation = value
