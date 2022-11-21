from handlers.filereader import FileReader

#    Väliaikainen konsolikäyttöliittymä     #
# ----------------------------------------- #
# Tätä käyttöliittymää on tarkoituksena     #
# käyttää ohjelman rungon kehityksen        #
# aikana. Saa itse ohjelman muuttujana,     #
# ja toteuttaa ohjelman metodeja riippuen   #
# komennosta.                               #

class Console:
    def __init__(self):

        # Osoite kansioon, josta tarkistetaan korttipakat automaattisesti
        self.__packfolder = "kortit"

        # Lista viiteistä avattuihin "valikoihin", jota
        # käytetään run()-loopissa
        self.__menu = [self.__mainmenu]

        
        

    # Palauttaa konsolin käytössä olevat komennot listana
    def __mainmenu(self) -> int:
        print("""\n-- KOMENNOT --
[a] avaa pakka
[x] poistu\n""")

        # Odota käyttäjältä komentoa
        command = input("> ")

        # Toteuta komento
        if command == "x": return -1
        if command == "a": self.__menu.append(self.__open)



    # -- Korttipakan avaamisvalikko --
    # Näyttää kansion /kortit/ korttipakat, ja antaa mahdollisuuden 
    # kirjoittaa korttipakan osoitteen manuaalisesti
    def __open(self):

        # Hae kansion .xmlpack-tiedostot, ja näytä ne listana
        files = FileReader.get_files(self.__packfolder, ".xmlpack", True)
        print(f"-- Korttipakat kansiossa /{self.__packfolder}/")

        # Näytä tiedostot listana komentorivillä muodossa "[index] tiedosto.xmlpack"
        for i in range(len(files)):
            print(f"[{i+1}] {files[i]}")

        if len(files) == 0: print("kansiosta ei löytynyt yhtään .xmlpack-tiedostoa")

        # Odota komentoa
        print("\nAnna numero avataksesi sitä vastaavan tiedoston")
        print(f"[m] osoite muu kuin /{self.__packfolder}/")
        print(f"[x] peruuta\n")

        while True:
            command = input(">")

            if command == "x": self.__menu.pop(); break
            if command.isnumeric() and int(command) <= len(files):
                print(files[int(command)-1])
                break;


            print("Tuntematon komento\n")



        


    # -- Aloita käyttöliittymän toteutus --
    def run(self):
        print("Väliaikainen konsolikäyttöliittymä")

        while True:
            # Toteuta nykyisen valikon toiminnallisuus, 
            # jos vastaus on -1, sulje konsolikäyttöliittymä
            if self.__menu[-1]() == -1:
                break
            




