
#    Väliaikainen konsolikäyttöliittymä     #
# ----------------------------------------- #
# Tätä käyttöliittymää on tarkoituksena     #
# käyttää ohjelman rungon kehityksen        #
# aikana. Saa itse ohjelman muuttujana,     #
# ja toteuttaa ohjelman metodeja riippuen   #
# komennosta.                               #

class Console:
    def __init__(self, service):

        # Sovellustoteutus
        self.__service = service

        # Lista viiteistä avattuihin "valikoihin", jota
        # käytetään run()-loopissa. Toimii jonona, jonka viimeinen
        # olio on nyt auki oleva valikko
        self.__menu = [self.__mainmenu]


    # Palauttaa konsolin käytössä olevat komennot listana
    def __mainmenu(self) -> int:
        print("""\n-- KOMENNOT --
[a] avaa pakka
[x] poistu\n""")

        # Odota käyttäjältä komentoa, ja toteuta se
        command = input("> ")

        if command == "x": return -1
        if command == "a": self.__menu.append(self.__open)



    # -- Korttipakan avaamisvalikko --
    # Näyttää kansion /kortit/ korttipakat, ja antaa mahdollisuuden 
    # kirjoittaa korttipakan osoitteen manuaalisesti
    def __open(self):

        print(f"-- Korttipakat kansiossa /{self.__service.packfolder}/")
        files = self.__service.get_files_in_folder()

        # Näytä tiedostot listana komentorivillä muodossa "[index] tiedosto.xmlpack"
        for i in range(len(files)):
            print(f"[{i+1}] {files[i]}")

        if len(files) == 0: print("kansiosta ei löytynyt yhtään .xmlpack-tiedostoa")

        # Odota komentoa
        print("\nAnna numero avataksesi sitä vastaavan tiedoston")
        #print(f"[m] osoite muu kuin /{self.__service.packfolder}/")
        print(f"[x] peruuta\n")

        while True:
            command = input(">")

            if command == "x": self.__menu.pop(); break

            # Lataa tiedosto jos käyttäjä antoi hyväksyyttävän numeron
            if command.isnumeric() and int(command) <= len(files):
                index = int(command)-1
                val = self.__service.load_pack(self.__service.packfolder + "/" +files[index])
                if val:
                    self.__menu.append(self.__cards)
                    return
                else:
                    print(self.__service.file_error + "\n")
                    continue


            print("Tuntematon komento\n")



    # -- Viikon 3 testifunktio, joka palauttaa jokaisen kortin pakassa -- #
    # Odottaa syötettä, jonka jälkeen palaa takaisin edelliseen valikkoon
    def __cards(self):
        print("Tulostetaan kaikki kortit:\n")
        while True:
            card = self.__service.get_next_card()
            if card == None: break

            print(f"{card.sentence}\nlukutapa: {card.reading} ({card.translation})\n")

        
        input("Paina ENTER jatkaaksesi.\n")
        self.__menu.pop()
        


        


    # -- Aloita käyttöliittymän toteutus --
    def run(self):
        print("Väliaikainen konsolikäyttöliittymä")

        while True:
            # Toteuta nykyisen valikon toiminnallisuus, 
            # jos vastaus on -1, sulje konsolikäyttöliittymä
            if self.__menu[-1]() == -1:
                break
            




