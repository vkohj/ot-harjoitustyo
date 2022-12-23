from tkinter import ttk
from ui.interfaces.template import TkinterGUITemplate


class TkinterGUICard(TkinterGUITemplate):
    """Korttien opiskeluikkuna. Käyttää TkinterGUITemplate-luokkaa runkona.
    """

    def __init__(self, window, service, handler):
        """Luokan konstruktori.

        Args:
            window (Tkinter.Tk): Tkinter-ikkuna.
            service (Flashcard): Sovellustoteutus.
            handler (TkinterGUI): Luokkaa käyttävä käyttöliittymän hallitsijaluokka.
        """

        super().__init__(window, service, handler)

        self.__card = None
        self.__card_turned = False

        self._service.generate_pack_random_order()
        self._initialize()


    def _reinitialize(self):
        """Uudelleenlataa jotkin valikon osat, joiden tiedot ovat voineet muuttua.
        """

        self._window.grid_rowconfigure(0, weight=10)
        self._window.grid_rowconfigure(0, weight=1)
        self._window.grid_columnconfigure(0, weight=1)


    def _initialize(self):
        """Luo korttien opiskeluun tarkoitetun valikon Tkinter-objektit
         ja lataa ensimmäisen kortin tiedot.
        """

        super()._initialize()
        self._reinitialize()

        frame = ttk.Frame(master=self._window, padding=(20, 20))
        self._add_elem(frame, 0, 0, sticky="NSEW")

        sentenceframe = ttk.Frame(frame)
        self._add_elem(sentenceframe, 0, 0, name="frame_sentence")
        self._add_elem(ttk.Label(
            sentenceframe, text="[SENTENCE", font=self._handler.font_sentence), 0, 0, name="label_sentence1", sticky="W")
        self._add_elem(ttk.Label(sentenceframe, text="**HIGHLIGHT**", font=self._handler.font_sentence_highlight,
                       foreground="#224894"), 1, 0, name="label_sentence2", sticky="W")
        self._add_elem(ttk.Label(sentenceframe, text="SENTENCE]",
                       font=self._handler.font_sentence), 2, 0, name="label_sentence3", sticky="W")

        self._add_elem(ttk.Label(
            frame, text="[READING]", font=self._handler.font_reading), 0, 1, name="label_reading", sticky="W")
        self._add_elem(ttk.Label(
            frame, text="[TRANSLATION]", font=self._handler.font_translation), 0, 2, name="label_translation", sticky="W")

        optionframe = ttk.Frame(self._window, padding=(20, 20))
        optionframe.grid_columnconfigure(0, weight=1)
        optionframe.grid_rowconfigure(0, weight=1)
        self._add_elem(optionframe, 0, 1, sticky="NSEW")

        self._add_elem(ttk.Button(optionframe, text="Seuraava",
                                  command=self.__next), 1, 0, name="button_next", sticky="NE")

        self._add_elem(ttk.Button(optionframe, text="Lopeta",
                                  command=self._exit), 0, 0, sticky="NE")

        self.__load_text()


    def __load_text(self):
        """Lataa nykyisen kortin tiedot valikkoon.
        Lukutapa ja käännöslause näytetään, jos TkinterGUICard.__card_turned on tosi.
        """

        if self.__card is None:
            self.__next()

        # Jaa lause **-merkkien perusteella
        sentences = self.__card.sentence.split("**")
        if len(sentences) != 3:
            sentences = [self.__card.sentence, "", ""]

        for i in range(3):
            text = ""
            if i < len(sentences):
                text = sentences[i]
            self._get_elem(f"label_sentence{i+1}").configure(text=text)

        # Tee toimintoja riippuen onko kortti käännetty vai ei
        if self.__card_turned:
            self._get_elem("label_reading").configure(text=self.__card.reading)
            self._get_elem("label_translation").configure(
                text=self.__card.translation)

            self._get_elem("button_next").configure(text="Seuraava")
        else:
            self._get_elem("label_reading").configure(text="")
            self._get_elem("label_translation").configure(text="")
            self._get_elem("button_next").configure(text="Näytä")


    def __next(self):
        """Näytä/seuraava -napin toiminto. Kääntää kortin, tai ottaa pakasta seuraavan kortin.
        Kutsuu sitten TkinterGUICard.__load_text()-metodia tekstin näyttämiseksi.
        """

        if self.__card_turned:
            self.__card = self._service.get_next_card()
            if self.__card is None:
                self._exit()
                return

            self.__card_turned = False
        else:
            self.__card_turned = True

        self.__load_text()
