#    Väliaikainen konsolikäyttöliittymä     #
# ----------------------------------------- #
# Tätä käyttöliittymää on tarkoituksena     #
# käyttää ohjelman rungon kehityksen        #
# aikana. Saa itse ohjelman muuttujana,     #
# ja toteuttaa ohjelman metodeja riippuen   #
# komennosta.                               #

class Console:
    def __init__(self):
        print("Väliaikainen konsolikäyttöliittymä")

    # Palauttaa konsolin käytössä olevat komennot listana
    def __commands(self) -> str:
        return ["KOMENNOT:", "[x]: poistu"]

    # Graafista käyttöliittymää vastaava while-loop
    def run(self):
        while True:
            print("\n".join(self.__commands()))

            # Odota käyttäjältä komentoa
            command = input("> ")

            if command == "x":
                break
            




