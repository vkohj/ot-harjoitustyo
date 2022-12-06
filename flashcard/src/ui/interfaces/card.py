from tkinter import ttk
from tkinter.font import Font
from ui.interfaces.template import TkinterGUITemplate


class TkinterGUICard(TkinterGUITemplate):
    def __init__(self, window, service, handler):
        super().__init__(window, service, handler)

        self.__card = None

        # Fontit
        self.__font_sentence = Font(size=12, weight="bold")
        self.__font_highlight = Font(size=12, underline=1, weight="bold")
        self.__font_reading = Font(size=11)
        self.__font_translation = Font(size=11)

        self._service.generate_pack_random_order()
        self.__initialize()

    def _reinitialize(self):
        self._window.grid_rowconfigure(0, weight=10)
        self._window.grid_rowconfigure(0, weight=1)
        self._window.grid_columnconfigure(0, weight=1)

    def __initialize(self):
        self._reinitialize()

        frame = ttk.Frame(master=self._window, padding=(20, 20))
        self._add_elem(frame, 0, 0, sticky="NSEW")

        sentenceframe = ttk.Frame(frame)
        self._add_elem(sentenceframe, 0, 0, name="frame_sentence")
        self._add_elem(ttk.Label(
            sentenceframe, text="[SENTENCE", font=self.__font_sentence), 0, 0, name="label_sentence1", sticky="W")
        self._add_elem(ttk.Label(sentenceframe, text="**HIGHLIGHT**", font=self.__font_highlight,
                       foreground="#224894"), 1, 0, name="label_sentence2", sticky="W")
        self._add_elem(ttk.Label(sentenceframe, text="SENTENCE]",
                       font=self.__font_sentence), 2, 0, name="label_sentence3", sticky="W")

        self._add_elem(ttk.Label(
            frame, text="[READING]", font=self.__font_reading), 0, 1, name="label_reading", sticky="W")
        self._add_elem(ttk.Label(
            frame, text="[TRANSLATION]", font=self.__font_translation), 0, 2, name="label_translation", sticky="W")

        optionframe = ttk.Frame(self._window, padding=(20, 20))
        optionframe.grid_columnconfigure(0, weight=1)
        optionframe.grid_rowconfigure(0, weight=1)
        self._add_elem(optionframe, 0, 1, sticky="NSEW")

        self._add_elem(ttk.Button(optionframe, text="Seuraava",
                                  command=self.__next), 1, 0, name="button_next", sticky="NE")

        self._add_elem(ttk.Button(optionframe, text="Lopeta",
                                  command=self._exit), 0, 0, sticky="NE")

        self.__next()

    def __next(self):
        if self.__card is None:
            self.__card = self._service.get_next_card()
            if self.__card is None:
                self._exit()
                return

            # Jaa lause **-merkkien perusteella
            sentences = self.__card.sentence.split("**")
            if len(sentences) != 3:
                sentences = [self.__card.sentence, "", ""]

            for i in range(3):
                text = ""
                if i < len(sentences):
                    text = sentences[i]
                self._get_elem(f"label_sentence{i+1}").configure(text=text)

            # self._get_elem("label_sentence").configure(text=self.__card.sentence)
            self._get_elem("label_reading").configure(text="")
            self._get_elem("label_translation").configure(text="")

            self._get_elem("button_next").configure(text="Näytä")

        else:
            self._get_elem("label_reading").configure(text=self.__card.reading)
            self._get_elem("label_translation").configure(
                text=self.__card.translation)

            self.__card = None
            self._get_elem("button_next").configure(text="Seuraava")
