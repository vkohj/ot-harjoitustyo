from tkinter import Tk
from ui.interfaces.open import TkinterGUIOpen


class TkinterGUI:
    def __init__(self, service):

        # Sovellusolio
        self.__service = service

        # Tkinter-oliot
        self.__window = Tk()
        self.__window.title("Flashcard")

        self.__menu = []

    def run(self):
        self.__menu.append(TkinterGUIOpen(self.__window, self.__service, self))

        self.__window.mainloop()

    def add_menu(self, menu):
        self.__menu[-1].hide()
        self.__menu.append(menu)
        menu.show()

    def pop_menu(self):
        self.__menu[-1].destroy()
        self.__menu.pop(-1)
        self.__menu[-1].show()
