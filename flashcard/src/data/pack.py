
class Pack:
    """Luokka, joka varastoi korttipakan sisältämät tiedot ja kortit.
    """

    def __init__(self, name, path):
        """Luokan konstruktori.

        Args:
            name (string): Korttipakan nimi.
            path (string): Korttipakan kuvaus.
        """

        self.__name = name
        self.__cards = []
        self.__path = path
        self.__unsaved_changes = False

    def add_card(self, card):
        """Lisää kortti pakkaan.

        Args:
            card (Card): Lisättävä kortti.
        """

        self.__cards.append(card)

    def get_card(self, index):
        """Ota korttipakasta kortti.

        Args:
            index (int): Kortin sijainti pakassa.

        Returns:
            Card: Kortti.
            None: Jos sijainnista ei löydy korttia.
        """

        if not self.exists(index):
            return None
        return self.__cards[index]

    def exists(self, index):
        """Palauttaa, onko index korttipakassa.

        Args:
            index (int): Kortin numero, jota etsitään.

        Returns:
            boolean: Onko index korttipakassa vai ei.
        """

        if index < 0 or index >= len(self.__cards):
            return False
        return True

    @property
    def name(self):
        return self.__name

    @property
    def path(self):
        return self.__path

    def __len__(self):
        """Antaa mahdollisuuden käyttää luokkaa len()-metodissa.

        Returns:
            int: Korttien määrä korttipakassa.
        """
        return len(self.__cards)

    # Property tallentamattomille pakan muutoksille
    def __get_unsaved_changes(self):
        """get/set-propertyn metodi.

        Returns:
            boolean: Palauttaa, onko korttipakkaan tehty muutoksia.
        """

        return self.__unsaved_changes

    def __set_unsaved_changes(self, value):
        """get/set-propertyn metodi.

        Args:
            value (boolean): Muuta korttipakkaan tehtyjä muutoksia esittävän muuttujan arvoa.
        """

        self.__unsaved_changes = value

    unsaved_changes = property(__get_unsaved_changes, __set_unsaved_changes)
