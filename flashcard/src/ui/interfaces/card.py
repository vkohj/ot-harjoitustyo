from tkinter import ttk
from ui.interfaces.template import TkinterGUITemplate

class TkinterGUICard(TkinterGUITemplate):
    def __init__(self, window, service, handler):
        super().__init__(window, service, handler)

        self.__card = None

        self._service.generate_pack_random_order()
        self.__initialize()

    def _reinitialize(self):
        self._window.grid_rowconfigure(0, weight=10)
        self._window.grid_rowconfigure(0, weight=1)
        self._window.grid_columnconfigure(0, weight=1)

    def __initialize(self):
        self._reinitialize()

        frame = ttk.Frame(master=self._window, padding=(20,20))
        self._add_elem(frame, 0, 0, sticky="NW")

        self._add_elem(ttk.Label(frame, text="[SENTENCE]"), 0, 0, name="label_sentence", sticky="W")
        self._add_elem(ttk.Label(frame, text="[READING]"), 0, 1, name="label_reading", sticky="W")
        self._add_elem(ttk.Label(frame, text="[TRANSLATION]"), 0, 2, name="label_translation", sticky="W")

        self._add_elem(ttk.Button(self._window, text="Seuraava",
            command=self.__next), 0, 1, sticky="SE", name="button_next")

        self.__next()

    def __next(self):
        if self.__card is None:
            self.__card = self._service.get_next_card()
            if self.__card is None:
                self._exit()
                return
            
            self._get_elem("label_sentence").configure(text=self.__card.sentence)
            self._get_elem("label_reading").configure(text="")
            self._get_elem("label_translation").configure(text="")

            self._get_elem("button_next").configure(text="Näytä")
            
        else:
            self._get_elem("label_reading").configure(text=self.__card.reading)
            self._get_elem("label_translation").configure(text=self.__card.translation)
            
            self.__card = None
            self._get_elem("button_next").configure(text="Seuraava")
