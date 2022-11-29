#    Sovelluksen käyttämä korttipakka-luokka     #
#   -----------------------------------------    #

class Pack:
    def __init__(self, name, path):
        self.__name = name
        self.__cards = []
        self.__path = path
        self.__unsaved_changes = False

    def add_card(self, card):
        self.__cards.append(card)

    def get_card(self, index):
        if index < 0 or index >= len(self.__cards):
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

    # Property tallentamattomille pakan muutoksille
    def __get_unsaved_changes(self):
        return self.__unsaved_changes

    def __set_unsaved_changes(self, value):
        self.__unsaved_changes = value

    unsaved_changes = property(__get_unsaved_changes, __set_unsaved_changes)
