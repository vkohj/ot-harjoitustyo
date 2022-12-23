from tkinter import ttk
from ui.interfaces.template import TkinterGUITemplate
from ui.interfaces.card import TkinterGUICard


class TkinterGUIPack(TkinterGUITemplate):
    """Pakkavalikko, jonka avulla voidaan opiskella kortteja, ja joka kertoo
    käyttäjälle, miten käynnistää konsolikäyttöliittymä korttien muokkaamista varten.
    Käyttää TkinterGUITemplate-luokkaa runkona.
    """

    def __init__(self, window, service, handler, pack_path):
        """Luokan konstruktori.

        Args:
            window (Tkinter.Tk): Tkinter-ikkuna.
            service (Flashcard): Sovellustoteutus.
            handler (TkinterGUI): Luokkaa käyttävä käyttöliittymän hallitsijaluokka.
            pack_path (string): Korttipakan osoite.
        """

        super().__init__(window, service, handler)

        self.__path = pack_path
        self.__pack = self._service.load_pack(self.__path)

        self._initialize()


    def _reinitialize(self):
        """Uudelleenlataa jotkin valikon osat, joiden tiedot ovat voineet muuttua.
        """

        self._window.grid_rowconfigure(0, weight=1)
        self._window.grid_columnconfigure(0, weight=1)


    def _initialize(self):
        """Luo valikon tarvittavat Tkinter-objektit, ja antaa virheilmoituksen, jos
        korttipakkaa ei ole ladattu oikein.
        """

        super()._initialize()
        self._reinitialize()

        outerframe = ttk.Frame(master=self._window)
        outerframe.grid_columnconfigure(0, weight=1)
        outerframe.grid_rowconfigure(0, weight=1)
        self._add_elem(outerframe, 0, 0, sticky="NSEW")

        frame = ttk.Frame(outerframe)
        self._add_elem(frame, 0, 0)

        # Lataa kortin tiedot
        if self.__pack is False:
            # Tulosta virheviesti
            label = ttk.Label(frame, text="Virhe", font=self._handler.font_h1)
            self._add_elem(label, 0, 0)
            label2 = ttk.Label(
                frame, text=f"{self._service.file_error}", font=self._handler.font_p)
            self._add_elem(label2, 0, 2)

            button = ttk.Button(frame, text="Takaisin", command=self._exit)
            self._add_elem(button, 0, 3)
            return

        # Tulosta vaihtoehdot
        self._add_elem(
            ttk.Label(frame, text=self._service.get_pack_name(), font=self._handler.font_h1), 0, 0)

        subframe = ttk.Frame(frame)
        self._add_elem(subframe, 0, 1)
        button = ttk.Button(subframe, text="Opiskele",
                       command=self.__study)
        self._add_elem(button, 0, 0)
        self._add_elem(ttk.Button(
            subframe, text="Takaisin", command=self._exit), 1, 0)

        self._add_elem(
            ttk.Label(frame, text="", font=self._handler.font_p), 0, 2)
        self._add_elem(ttk.Label(
            frame, text="Muokkaus saatavilla vain konsolikäyttöliittymässä.",
                font=self._handler.font_p), 0, 3)
        self._add_elem(ttk.Label(
            frame, text='"poetry run invoke console" tai "poetry run python src --console"',
                font=self._handler.font_p), 0, 4)

        # Jos kortteja ei ole pakassa, sammuta "Opiskele"-nappi ja lisää teksti
        if len(self._service.get_sentences()) == 0:
            button.configure(state="disable")
            self._add_elem(ttk.Label(frame, text="", font=self._handler.font_p), 0, 5)
            self._add_elem(ttk.Label(
            frame, text="*Opiskeleminen ei ole saatavilla, koska pakassa ei ole yhtään korttia.",
                font=self._handler.font_p), 0, 6)


    def __study(self):
        """Käskee käyttöliittymän hallinnoijaa avamaan korttien opiskeluikkunan.
        """

        self._handler.add_menu(TkinterGUICard(
            self._window, self._service, self._handler))
