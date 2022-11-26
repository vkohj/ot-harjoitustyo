from ui.console import Console
from flashcard import Flashcard

def main():
    # Luo sovellus-luokka
    service = Flashcard()

    # Käytä väliaikaista konsolikäyttöliittymää
    console = Console(service)
    console.run()

if __name__ == "__main__":
    main()
