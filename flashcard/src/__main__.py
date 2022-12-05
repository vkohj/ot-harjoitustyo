import sys

from ui.console import Console
from ui.tkinter import TkinterGUI
from flashcard import Flashcard

def main():
    # Luo sovellus-luokka
    service = Flashcard()

    # Tarkista, halutaanko avata konsolikäyttöliittymä
    if "--console" in sys.argv:
        console = Console(service)
        console.run()
    else:
        interface = TkinterGUI(service)
        interface.run()



if __name__ == "__main__":
    main()
