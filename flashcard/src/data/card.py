class Card:
    def __init__(self, sentence, reading, translation):
        self.__sentence = sentence
        self.__reading = reading
        self.__translation = translation

    @property
    def sentence(self):
        return self.__sentence

    @property
    def reading(self):
        return self.__reading
    
    @property
    def translation(self):
        return self.__translation

    
    
    