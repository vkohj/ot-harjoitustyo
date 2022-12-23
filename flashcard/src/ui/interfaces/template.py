class TkinterWidgetTemplate:
    """Käytetään Tkinter-käyttöliittymäobjektien asetusten varastoimiseen.
    Käytännöllinen valikkoja piilottaessa.
    """

    def __init__(self, widget, column, row, sticky):
        """Luokan konstruktori

        Args:
            widget: Tkinter-objekti
            column (int): Pylväs, jolla objekti sijaitsee
            row (int): Rivi, jolla objekti sijaitsee
            sticky (string): Tkinterin sticky-asetus
        """

        self.widget = widget
        self.column = column
        self.row = row
        self.sticky = sticky


class TkinterGUITemplate:
    """Käyttöliittymän valikon runko, jota käytetään valikkoluokissa (kuten card.py, open.py, pack.py)
    """

    def __init__(self, window, service, handler):
        """Luokan konstruktori.

        Args:
            window (Tkinter.Tk): Tkinter-ikkuna.
            service (Flashcard): Sovellustoteutus.
            handler (TkinterGUI): Luokkaa käyttävä käyttöliittymän hallitsijaluokka.
        """

        self._window = window
        self._service = service
        self._handler = handler

        # Status
        self._hidden = False

        # Elementit
        self.__elem = []
        self.__elem_named = {}


    def destroy(self):
        """Tuhoa valikon tallentamat Tkinter-objektit.
        """

        for elem in self.__elem:
            elem.widget.destroy()

        for elem in self.__elem_named.values():
            elem.widget.destroy()

        self.__elem.clear()
        self.__elem_named.clear()


    def _reinitialize(self):
        """Uudelleenlataa jotkin valikon osat, joiden tiedot ovat voineet muuttua.

        Raises:
            NotImplementedError: Metodia ei tule käyttää rungon kautta.
        """

        raise NotImplementedError("Must override in child class")


    def rebuild(self):
        """Lataa valikko kokonaan uudelleen tuhoamalla kaikki objektit, ja luomalla ne uudelleen.
        """

        self.destroy()
        self._initialize()


    def hide(self):
        """Piilota valikko poistamalla kaikki valikon objektit grid-objekteistaan.
        """

        if self._hidden:
            return

        for elem in self.__elem:
            elem.widget.grid_forget()

        for elem in self.__elem_named.values():
            elem.widget.grid_forget()

        self._hidden = True


    def show(self):
        """Näytä valikko lisäämällä Tkinter-objektit takaisin grid-objektiinsa.
        """

        if not self._hidden:
            return

        self._reinitialize()

        for elem in self.__elem:
            elem.widget.grid(column=elem.column,
                             row=elem.row, sticky=elem.sticky)

        for elem in self.__elem_named.values():
            elem.widget.grid(column=elem.column,
                             row=elem.row, sticky=elem.sticky)

        self._hidden = False


    def _initialize(self):
        """Rungon asetukset asettava funktio.
        """

        self._window.minsize(800, 400)


    def _add_elem(self, elem, column, row, sticky="", name=""):
        """Lisää Tkinter-objekti valikkoon sen oikeaan kohtaan, ja tallenna se valikon listaan.

        Args:
            elem: Tkinter-objekti.
            column (int): Pylväs.
            row (int): Rivi.
            sticky (str, optional): Tkinterin sticky-asetus. Defaults to "".
            name (str, optional): Tallenna listaan nimellä. Defaults to "".

        Raises:
            IndexError: Jos nimi on jo käytössä listalla.
        """

        to_append = TkinterWidgetTemplate(elem, column, row, sticky)

        if name == "":
            self.__elem.append(to_append)
        else:
            if name in self.__elem_named.keys():
                raise IndexError(f"Element already exists in [{name}]")
            self.__elem_named[name] = to_append

        if not self._hidden:
            elem.grid(row=row, column=column, sticky=sticky)


    def _get_elem(self, name):
        """Palauta nimetty objekti tallennettujen objektien listalta.

        Args:
            name (str): Nimi.

        Returns:
            Palauttaa Tkinter-objektin.
            None: Jos objektia ei löytynyt.
        """
        if name in self.__elem_named:
            return self.__elem_named[name].widget
        return None


    def _exit(self):
        """Pyytää käyttöliittymän hallitsijaa poistamaan ylimmän (nyt käytössä olevan) valikkonsa.
        """

        self._handler.pop_menu()
