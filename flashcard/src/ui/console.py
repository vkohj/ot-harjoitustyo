
class Console:
    """Väliaikainen konsolikäyttöliittymä.

    Yksi kahdesta Flashcard-ohjelman käyttöliittymästä, jota
     on enemmänkin tarkoitus käyttää rungon kehityksen aikana.
    """

    def __init__(self, service):
        """Luokan konstruktori.

        Args:
            service (Flashcard): Ohjelmatoteutus
        """

        self.__service = service
        self.__menu = [self.__open]


    def __open(self):
        """Korttipakan avaamisvalikko, joka näyttää ja antaa käyttäjän
        valita Flashcard-luokan korttikansion korttipakoista.
        """

        print(f"-- Korttipakat kansiossa /{self.__service.packfolder}/")
        files = self.__service.get_files_in_folder()

        # Näytä tiedostot listana komentorivillä muodossa "[index] tiedosto.xmlpack"
        for i, file in enumerate(files):
            print(f"[{i+1}] {file}")

        if len(files) == 0:
            print("kansiosta ei löytynyt yhtään .xmlpack-tiedostoa")

        print("\nAnna numero avataksesi sitä vastaavan tiedoston")
        print("[x] sulje")

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


    def __cards(self):
        """Valikko ohjelman ladattua korttipakan.
        """

        print(f'''Pakan "{self.__service.get_pack_filename()}" komennot:''')

        if self.__service.get_pack_changed():
            print("(tallentamaton)")

        print('''\n[o] opiskele
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


    def __study(self):
        """Valikko korttipakan korttien opiskeluun
        """

        self.__service.generate_pack_random_order()

        while True:
            card = self.__service.get_next_card()
            if card is None:
                break

            print("\n" + card.sentence)
            input()
            print(card.reading + "\n" + card.translation + "\n")

        input("Pääsit korttipakan loppuun.\nPaina ENTER jatkaaksesi.\n>")
        self.__menu.pop()


    def __print_cards(self):
        """Valikko, joka tulostaa korttipakan kaikki kortit niiden lineaarisessa järjestyksessä.
        """

        self.__service.generate_pack_linear_order()

        print("Tulostetaan kaikki kortit:\n")
        while True:
            card = self.__service.get_next_card()
            if card is None:
                break

            print(f"{card.sentence}\nlukutapa: {card.reading} ({card.translation})\n")

        input("Paina ENTER jatkaaksesi.\n>")
        self.__menu.pop()


    def __modify(self):
        """Korttipakan muokkaukseen tarkoitettu valikko
        """

        while True:
            print("Komentojen formaatti: <komento> (kortin numero)")
            print(
                "[list]: listaa kortit, [add] lisää, [edit <n>] muokkaa, [save] tallenna, [x] poistu")

            command = input(">")
            commands = command.split(" ")

            if command == "x":
                if self.__service.get_pack_changed():
                    self.__linear_save()
                self.__menu.pop()
                break

            if command == "list":
                sentences = self.__service.get_sentences()

                for i, sentence in enumerate(sentences):
                    print(f"[{i+1}] {sentence}")
                print()
                continue

            if command == "add":
                self.__linear_add()
                return

            if len(commands) == 2:
                if commands[0] == "edit":
                    if not commands[1].isnumeric():
                        print(f"{commands[1]} ei ole numero")
                        continue

                    index = int(commands[1])-1
                    self.__linear_edit(index)
                    continue

            if command == "save":
                self.__linear_save()
                continue

            print("Tuntematon komento\n")


    def run(self):
        """Aloittaa käyttöliittymän toteutusloopin. Palautuu, kun Console.__menu-lista on tyhjä.
        """

        print("Väliaikainen konsolikäyttöliittymä\n")

        while True:
            if len(self.__menu) == 0:
                break

            # Toteuta nykyisen valikon toiminnallisuus,
            # jos vastaus on -1, sulje konsolikäyttöliittymä
            if self.__menu[-1]() == -1:
                break


    def __linear_edit(self, index):
        """Lineaarinen kortin muutosikkuna, jota ei lisätä Console.__menu-listaan

        Args:
            index (int): Kortin paikka listassa.
        """

        if index < 0 or index >= len(self.__service.get_sentences()):
            print(f"Ei korttia kohdassa {index+1}\n")
            return

        # Pyydä käyttäjältä uudet arvot
        sentence = self.__func_edit_value(
            "Lause", self.__service.get_card_sentence(index), True)
        reading = self.__func_edit_value(
            "Lukutapa", self.__service.get_card_reading(index))
        translation = self.__func_edit_value(
            "Käännös", self.__service.get_card_translation(index))

        # Muuta lause
        if self.__linear_update_question(sentence, reading, translation):
            self.__service.set_card_sentence(index, sentence)
            self.__service.set_card_reading(index, reading)
            self.__service.set_card_translation(index, translation)

            print("Tiedot muutettiin\n")
        else:
            print("Peruutetaan\n")


    def __linear_update_question(self, sentence, reading, translation):
        """Lineaarinen kortin päivittämisen varmistusikkuna, jota ei lisätä Console.__menu-listaan

        Args:
            sentence (string): Kortin lause.
            reading (string): Kortin lukutapa.
            translation (string): Kortin käännöslause.

        Returns:
            True: Käyttäjä hyväksyy muutokset
            False: Käyttäjä ei hyväksynyt muutoksia
        """

        print("Kortin päivitetyt tiedot")
        print(f"Lause: {sentence}")
        print(f"Lukutapa: {reading}")
        print(f"Käännös: {translation}")

        print("\nOvatko nämä oikein? ([y] hyväksy, [n]/tyhjä peruuta)")
        command = input(">")
        if command == "y":
            return True
        return False


    def __linear_save(self):
        """Lineaarinen kortin tallennusikkuna, jota ei lisätä Console.__menu-listaan.

        Tallentaa listan, jos käyttäjä varmistaa haluavansa tallentaa listan.
        """

        print(
            f"Haluatko tallentaa pakan tiedostoon {self.__service.get_pack_filename()}?")
        print("([y] hyväksy, [n]/tyhjä peruuta)")
        command = input(">")

        if command == "y":
            if self.__service.save_pack() is False:
                print(self.__service.file_error + "\n")
            else:
                print("Tallennettu\n")
            return

        print("Peruutetaan\n")


    def __linear_add(self):
        """Lineaarinen kortin lisäämisen valikko, jota ei lisätä Console.__menu-listaan.

        Muokkaa Flashcard-luokan aktiivisen korttipakan kortteja."""

        sentence = self.__func_new_value("Lause", True)
        if sentence is None:
            return

        reading = self.__func_new_value("Lukutapa")
        if reading is None:
            return

        translation = self.__func_new_value("Käännös")
        if translation is None:
            return

        if self.__linear_update_question(sentence, reading, translation):
            if self.__service.new_card(sentence, reading, translation):
                print("Tiedot lisättiin\n")
            else:
                print("Virhe tapahtui lisätessä korttia pakkaan")
        else:
            print("Peruutetaan\n")


    def __func_edit_value(self, typename, default, require_highlight=False):
        """Monesti käytettävä käyttöliittymän osa,
        joka tulostaa nykyisen muuttujan ja kysyy käyttäjältä uutta muuttujaa.

        Args:
            typename (string): Lauseen tyyppi
            default (string): Nykyinen lause
            require_highlight (bool, optional): Vaatiiko, että lause sisältää kohdan,
            joka on ympyröity **-merkeillä. Defaults to False.

        Returns:
            string: Palauttaa joko alkuperäisen lauseen tai uuden lauseen
        """

        print(f"{typename}: {default}")
        value = input("Uusi lause (tyhjä = jatka muuttamatta): ")
        if value != "":
            if require_highlight and not self.__func_has_highlight(value):
                return default

            print("")
            return value
        print("")
        return default


    def __func_new_value(self, typename, require_highlight=False):
        """Monesti käytettävä käyttöliittymän osa, joka pyytää käyttäjältä uutta muuttujaa.

        Args:
            typename (string): Muuttujan tyyppi
            require_highlight (bool, optional): Vaatiiko, että lause sisältää kohdan,
            joka on ympyröity **-merkeillä. Defaults to False.

        Returns:
            string: Uusi muuttuja.
            None: Jos muuttuja on tyhjä tai se ei sisällä **-merkeillä ympäröityä kohtaa.
        """

        value = input(f"{typename}: ")
        if value == "":
            print("Peruutetaan\n")
            return None

        if require_highlight and not self.__func_has_highlight(value):
            return None

        print("")
        return value


    def __func_has_highlight(self, string):
        """Monesti käytettävä käyttöliittymän osa, joka testaa, onko lause ympäröity **-merkeillä.

        Args:
            string (string): Testattava lause.

        Returns:
            boolean: Onko jokin lauseen osa ympäröity **-merkeillä.
        """

        if string.count("**") != 2:
            print("Syöte ei sisältänyt **-merkeillä ympäröityä aluetta\n")
            return False
        if len(string.split("**")[1]) == 0:
            print("**-merkeillä ympäröity alue ei sisältänyt yhtään kirjainta\n")
            return False

        return True
