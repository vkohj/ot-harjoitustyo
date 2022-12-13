class Card:
    """Luokka, joka varastoi korttipakassa olevan kortin tiedot.
    """

    def __init__(self, sentence, reading, translation):
        """Konstruktori, joka luo Card-objektin ja antaa sille siihen kuuluvat arvot.

        Args:
            sentence (string): Japaninkielinen lause
            reading (string): Lukutapa
            translation (string): Käännöslause
        """

        self.__sentence = sentence
        self.__reading = reading
        self.__translation = translation

    def __get_sentence(self):
        """get/set-propertyn käyttämä metodi.

        Returns:
            string: Palauttaa japaninkielisen lauseen.
        """

        return self.__sentence

    def __set_sentence(self, value):
        """get/set-propertyn käyttämä metodi.

        Args:
            value (string): Japaninkielinen lause
        """

        if value == "":
            return
        self.__sentence = value

    def __get_reading(self):
        """get/set-propertyn käyttämä metodi.

        Returns:
            string: Palauttaa kortin lukutavan.
        """

        return self.__reading

    def __set_reading(self, value):
        """get/set-propertyn käyttämä metodi.

        Args:
            value (string): Lukutapa
        """

        if value == "":
            return
        self.__reading = value

    def __get_translation(self):
        """get/set-propertyn käyttämä metodi.

        Returns:
            string: Palauttaa kortin käännöslauseen.
        """

        return self.__translation

    def __set_translation(self, value):
        """get/set-propertyn käyttämä metodi.

        Args:
            value (string): Käännöslause.
        """

        if value == "":
            return
        self.__translation = value

    sentence = property(__get_sentence, __set_sentence)
    reading = property(__get_reading, __set_reading)
    translation = property(__get_translation, __set_translation)
