#    Sovelluksen käyttämä korttipakka-luokka     #
#   -----------------------------------------    #

class Pack:
    def __init__(self, name):
        self.__name = name
        self.__cards = []

    def add_card(self, card):
        self.__cards.append(card)

    def get_card(self, index):
        if index >= len(self.__cards):
            return None
        return self.__cards[index]

    @property
    def get_name(self):
        return self.__name
