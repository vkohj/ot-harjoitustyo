from tkinter import Tk, Toplevel, Menu, constants, ttk, font
from ui.interfaces.open import TkinterGUIOpen


class TkinterGUI:
    def __init__(self, service):
        """Toinen Flashcard-sovelluksen käyttöliittymistä. Graafinen pääkäyttöliittymä, joka 

        Args:
            service (Flashcard): Sovellustoteutus.
        """

        self.__service = service

        # Tkinter-oliot
        self.__window = Tk()
        self.__window.title("Flashcard")
        self.__window.option_add('*tearOff', False)

        self.__menu = []
        self.__settings_objects = []

        self.__reload_settings()
        self.init_menubar()
    
    def __reload_settings(self):
        """Lataa käyttöliittymän asetukset, kuten fontit.
        """

        family = self.__service.get_setting("font_family")

        self.font_h1 = font.Font(family=family, size=self.__service.get_setting("font_h1"), weight="bold")
        self.font_p = font.Font(family=family, size=self.__service.get_setting("font_p"))
        self.font_p_underline = font.Font(family=family, size=self.__service.get_setting("font_p"), underline=1)

        self.font_sentence = font.Font(family=family, size=self.__service.get_setting("font_sentence"))
        self.font_sentence_highlight = font.Font(family=family, size=self.__service.get_setting("font_sentence"), weight="bold")
        self.font_translation = font.Font(family=family, size=self.__service.get_setting("font_translation"))
        self.font_reading = font.Font(family=family, size=self.__service.get_setting("font_reading"))


    def init_menubar(self):
        """Alustaa käyttöliittymän valikon.
        """

        menu = Menu(self.__window)
        self.__window['menu'] = menu

        menu.add_command(label='Avaa')
        menu.entryconfigure('Avaa', state=constants.DISABLED)
        menu.add_command(label='Asetukset', command=self._popup_setting)

    def run(self):
        """Aloittaa käyttöliittymän toteutusloopin.
        """

        self.__menu.append(TkinterGUIOpen(self.__window, self.__service, self))

        self.__window.mainloop()

    def add_menu(self, menu):
        """Lisää valikko TkinterGUI.__menu-listaan.

        Args:
            menu (TkinterGUITemplate): Valikko
        """

        self.__menu[-1].hide()
        self.__menu.append(menu)
        menu.show()

    def pop_menu(self):
        """Tuhoa viimeisin valikko listalta.
        """

        self.__menu[-1].destroy()
        self.__menu.pop(-1)
        self.__menu[-1].show()

    def __reload_menus(self):
        """Uudelleenalusta kaikki TkinterGUI.__menu-listan valikot.
        """

        for menu in self.__menu:
            menu.rebuild()

    def _popup_setting(self):
        """Asetukset-popup valikon alustava metodi. Tuhotaan vanha aina, kun avataan uudelleen.
        """

        if len(self.__settings_objects) > 0:
            for val in self.__settings_objects.values():
                val.destroy()
            self.__settings_objects.clear()

        top= Toplevel(self.__window)
        top.grab_set()
        top.minsize(350, 400)
        top.maxsize(350, 400)
        top.title("Asetukset")
        top.grid_columnconfigure(0, weight=1)
        top.grid_rowconfigure(0, weight=1)

        frame = ttk.Frame(master=top, padding=(20, 20, 20, 20))
        frame.grid(row=0, column=0, sticky="NSEW")
        frame.grid_columnconfigure(0, weight=4)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(9, weight=1)

        # Fontin valinta
        ttk.Label(frame, text="Fontti", font=self.font_p).grid(column=0, row=0, columnspan=2, sticky="W")

        fonts = font.families()
        w_font_family = ttk.Combobox(frame, values=fonts)
        w_font_family.grid(column=0, row=1, columnspan=2, sticky="WE")

        fnt = self.__service.get_setting('font_family')
        if fnt is None:
            fnt = ""
        w_font_family.insert(0, fnt)

        ttk.Label(frame).grid(row=2, column=0)

        # Fonttikoot
        w_font_h1 = self.__setting_font_size_widget(frame, 
            "Otsikon fonttikoko", 3, self.__service.get_setting('font_h1'), 10, 22)
        w_font_p = self.__setting_font_size_widget(frame, 
            "Tekstin fonttikoko", 4, self.__service.get_setting('font_p'), 6, 22)

        ttk.Label(frame).grid(row=5, column=0)

        w_font_sentence = self.__setting_font_size_widget(frame, 
            "Lauseen fonttikoko", 6, self.__service.get_setting('font_sentence'), 6, 22)
        w_font_reading = self.__setting_font_size_widget(frame, 
            "Lukutavan fonttikoko", 7, self.__service.get_setting('font_reading'), 6, 22)
        w_font_translation = self.__setting_font_size_widget(frame, 
            "Käännöksen fonttikoko", 8, self.__service.get_setting('font_translation'), 6, 22)

        # Tallennusnappi
        w_save_button = ttk.Button(frame, text="Tallenna muutokset", command=self.__setting_save)
        w_save_button.grid(row=9, column=0, columnspan=2, sticky="S")

        # Lisätään tärkeät objektit listaan
        self.__settings_objects = {"top":top, "w_save_button":w_save_button, "w_font_family":w_font_family, "w_font_h1":w_font_h1, "w_font_p":w_font_p,
            "w_font_sentence":w_font_sentence, "w_font_reading":w_font_reading, "w_font_translation":w_font_translation}


    def __setting_save(self):
        """Asetusikkunan tallenusmetodi, joka antaa tallennetut muutokset Flashcard-luokalle.
        """
        
        self.__service.set_setting("font_family", self.__settings_objects["w_font_family"].get())

        self.__setting_save_numeric("font_h1", self.__settings_objects["w_font_h1"].get())
        self.__setting_save_numeric("font_p", self.__settings_objects["w_font_p"].get())
        self.__setting_save_numeric("font_sentence", self.__settings_objects["w_font_sentence"].get())
        self.__setting_save_numeric("font_reading", self.__settings_objects["w_font_reading"].get())
        self.__setting_save_numeric("font_translation", self.__settings_objects["w_font_translation"].get())

        self.__service.save_setting()
        self.__reload_settings()
        self.__reload_menus()

        # Uudelleenkäynnistä asetusikkuna
        self.__settings_objects["w_font_sentence"].destroy()
        self._popup_setting()


    def __setting_save_numeric(self, key, value):
        """Usein käytetty asetusten tallentamisen metodi, joka tarkistaa onko arvo numero, ja onko se väliltä 6 - 22

        Args:
            key (string): asetuksen avain
            value (string): testattava lause
        """

        if value.isnumeric() and int(value) >= 6 and int(value) <= 22:
            self.__service.set_setting(key, value)


    def __setting_font_size_widget(self, frame, name, row, value, from_, to_):
        """Usein käytetty metodi, joka luo asetusikkunassa käytetyn rivin, jossa vasemmalla on teksti ja oikealla Spinbox-widget.

        Args:
            frame (tkk.Frame): Isäntä
            name (string): Vasemmalla oleva teksti
            row (int): Rivi isännässä
            value (int): Alustava arvo Spinbox-luokalle
            from_ (int): Pienin hyväksyttävä arvo
            to_ (int): Suurin hyväksyttävä arvo

        Returns:
            ttk.Spinbox: Palauttaa luodun ttk.Spinbox-objektin.
        """

        txt = ttk.Label(frame, text=name, font=self.font_p)
        txt.grid(row=row, column=0, sticky="W")

        change = ttk.Spinbox(frame, width=4, from_=from_, to_=to_)
        change.grid(row=row, column=1, sticky="E")
        change.insert(0, value)

        return change
