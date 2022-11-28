
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
        self.__menu = [self.__open]

    # -- Korttipakan avaamisvalikko --
    # Näyttää kansion /kortit/ korttipakat, ja antaa mahdollisuuden
    # kirjoittaa korttipakan osoitteen manuaalisesti
    def __open(self):

        print(f"-- Korttipakat kansiossa /{self.__service.packfolder}/")
        files = self.__service.get_files_in_folder()

        # Näytä tiedostot listana komentorivillä muodossa "[index] tiedosto.xmlpack"
        for i in range(len(files)):
            print(f"[{i+1}] {files[i]}")

        if len(files) == 0:
            print("kansiosta ei löytynyt yhtään .xmlpack-tiedostoa")

        # Odota komentoa
        print("\nAnna numero avataksesi sitä vastaavan tiedoston")
        #print(f"[m] osoite muu kuin /{self.__service.packfolder}/")
        print(f"[x] sulje")

        while True:
            command = input(">")

            if command == "x":
                self.__menu.pop()
                break

            # Lataa tiedosto jos käyttäjä antoi hyväksyyttävän numeron
            if command.isnumeric() and int(command) <= len(files):
                index = int(command)-1
                val = self.__service.load_pack(
                    self.__service.packfolder + "/" + files[index])
                if val:
                    self.__menu.append(self.__cards)
                    return
                else:
                    print(self.__service.file_error + "\n")
                    continue

            print("Tuntematon komento\n")

    # -- Kun ohjelma on avannut pakan, kysy mitä pakalla tehdään -- #
    def __cards(self):
        print(f'''Pakan "{self.__service.get_pack_filename()}" komennot:\n
[o] opiskele
[m] muokkaa
[l] korttilista
[x] peruuta''')

        while True:
            command = input(">")
            if command == "x":
                self.__menu.pop()
                return

            if command == "o":
                self.__menu.append(self.__study)
                return

            if command == "m":
                self.__menu.append(self.__modify)
                return

            if command == "l":
                self.__menu.append(self.__print_cards)
                return

    # -- Korttien opiskelu -- #
    def __study(self):
        # Aseta kortit satunnaiseen järjestykseen
        self.__service.generate_pack_random_order()

        while True:
            card = self.__service.get_next_card()
            if card == None:
                break

            print("\n" + card.sentence)
            input()
            print(card.reading + "\n" + card.translation + "\n")


        input("Pääsit korttipakan loppuun.\nPaina ENTER jatkaaksesi.\n>")
        self.__menu.pop()

    # -- Tulostaa pakan kortit --
    def __print_cards(self):
        # Aloita korttien lukeminen alusta
        self.__service.generate_pack_linear_order()

        print("Tulostetaan kaikki kortit:\n")
        while True:
            card = self.__service.get_next_card()
            if card == None:
                break

            print(f"{card.sentence}\nlukutapa: {card.reading} ({card.translation})\n")

        input("Paina ENTER jatkaaksesi.\n>")
        self.__menu.pop()

    # -- Muokkaa korttipakkaa --
    def __modify(self):
        while True:
            print("Komentojen formaatti: <komento> (kortin numero)")
            print("[list]: listaa kortit  [edit <n>] muokkaa  [x] poistu")

            command = input(">")
            commands = command.split(" ")

            if command == "x":
                self.__menu.pop()
                break
            
            if command == "list":
                sentences = self.__service.get_sentences()
                for i in range(len(sentences)):
                    print(f"[{i+1}] {sentences[i]}")
                print()
                continue

            if len(commands) == 2:
                if commands[0] == "edit":
                    if commands[1].isnumeric() == False:
                        print(f"{commands[1]} ei ole numero")
                        continue

                    index = int(commands[1])-1
                    if i < 0 or i >= len(sentences):
                        print(f"Ei korttia kohdassa {commands[1]}")

                    # Lause
                    sentence = self.__service.get_card_sentence(index)
                    print(f"Lause: {sentence}")
                    value = input("Uusi lause (tyhjä = jatka muuttamatta): ")
                    if value != "":
                        sentence = value

                    # Muuta lause
                    # TODO: vaadi varmistus muutoksista
                    self.__service.set_card_sentence(index, sentence)

                    continue

            print("Tuntematon komento\n")

    # -- Aloita käyttöliittymän toteutus --
    def run(self):
        print("Väliaikainen konsolikäyttöliittymä\n")

        while True:
            if len(self.__menu) == 0:
                break

            # Toteuta nykyisen valikon toiminnallisuus,
            # jos vastaus on -1, sulje konsolikäyttöliittymä
            if self.__menu[-1]() == -1:
                break
