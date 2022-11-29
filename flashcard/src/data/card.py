class Card:
    def __init__(self, sentence, reading, translation):
        self.__sentence = sentence
        self.__reading = reading
        self.__translation = translation

    def __get_sentence(self):
        return self.__sentence

    def __set_sentence(self, value):
        if value == "":
            return
        self.__sentence = value

    def __get_reading(self):
        return self.__reading

    def __set_reading(self, value):
        if value == "":
            return
        self.__reading = value

    def __get_translation(self):
        return self.__translation

    def __set_translation(self, value):
        if value == "":
            return
        self.__translation = value

    sentence = property(__get_sentence, __set_sentence)
    reading = property(__get_reading, __set_reading)
    translation = property(__get_translation, __set_translation)
