#    Sovelluksen käyttämä korttipakka-luokka     #
#   -----------------------------------------    #

class Pack:
    def __init__(self, name, path):
        self.__name = name
        self.__cards = []
        self.__path = path

    def add_card(self, card):
        self.__cards.append(card)

    def get_card(self, index):
        if index >= len(self.__cards):
            return None
        return self.__cards[index]

    @property
    def name(self):
        return self.__name

    @property
    def path(self):
        return self.__path

    def __len__(self):
        return len(self.__cards)
