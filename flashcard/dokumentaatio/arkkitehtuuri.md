# Sovelluksen arkkitehtuuri
## Rakenne
Sovellus perustuu käyttöliittymän (kuvassa Console-luokka) ja Flashcard-luokan väliseen yhteistyöhön. Käyttöliittymä pyytää ainoastaan tarvittavat tiedot Flashcard-luokalta, joka suorittaa kortteihin liittyvät muutokset ja koordinoi niiden lataamisen ja tallentamisen yhdessä FileReader-luokan kanssa.

```mermaid
    classDiagram
        Console "0..1" --> "" Flashcard
        Flashcard "" --> "0..1" Pack
        Flashcard "" --> "1" FileReader
        Pack "" --> "*" Card
        
```

## Kansio- ja tiedostorakenne
Ohjelman rakenne on jaettu kolmeen luokkaan
* ui (sisältää eri käyttöliittymät)
    * interfaces (sisältää tkinter näkymien luokat)
* data (sisältää ainoastaan tietoa varastoivat luokat)
* handlers (erityisesti tiedonkäsittelyyn tarkoitetut luokat)

Pääkansiosta löytyy kaksi merkittävää tiedostoa: \_\_main__.py ja flashcard.py. 

\_\_main__.py -tiedosto on ohjelman käynnistystiedosto, joka luo Flashcard- ja jonkin käyttöliittymäluokan. flashcard.py -tiedosto taas sisältää itse Flashcard-luokan ohjelmakoodin.

```mermaid
    flowchart TB
    
    subgraph flashcard
        flashcard.py
        __main__.py
    end

    subgraph ui
        console.py
        tkinter.py
    end

    subgraph interfaces
        card.py
        open.py
        pack.py
        template.py
    end

    subgraph data
        pack.py
        card.py
    end

    subgraph handlers
        filereader.py
    end

    flashcard --> ui
    flashcard --> data
    flashcard --> handlers
    ui --> interfaces
        
```


## Pakan lataaminen
Käyttöliittymä pyytää pakan lataamista Flashcard-luokalta, joka toimii yhteistyössä staattisen FileReader-luokan kanssa .xmlpack tiedostojen lukemisessa.

Ensin pyydetään listaa "kortit"-kansion .xmlpack tiedostoista, jonka jälkeen ladataan pakka "pakka1.xmlpack"

Alemmassa kuvassa oletetaan, että pakka1 sisältää kaksi korttia. UI tarkoittaa jotain käyttöliittymäluokkaa (kuten Console tai TkinterGUI)

```mermaid
sequenceDiagram

  actor käyttäjä

  participant UI
  participant Flashcard
  participant FileReader
  participant pakka

  UI->>Flashcard: get_files_in_folder("kortit")
  Flashcard->>FileReader: get_files("kortit", ".xmlpack", True)
  FileReader->>Flashcard: ["pakka1.xmlpack", "pakka2.xmlpack"]
  Flashcard->>UI: ["pakka1.xmlpack", "pakka2.xmlpack"]

  käyttäjä->>UI: valitsee jonkin pakoista
  UI->>Flashcard: load_pack("kortit/pakka1.xmlpack")
  Flashcard->>FileReader: load_from_xml("kortit/pakka1.xmlpack")
  FileReader->>pakka: Pack(name, "kortit/pakka1.xmlpack")
  FileReader->>pakka: add_card(sentence, reading, translation)
  FileReader->>pakka: add_card(sentence, reading, translation)
  FileReader->>Flashcard: pakka
  Flashcard->>Flashcard: generate_pack_linear_order()
  Flashcard->>UI: True
```

Lataamisen jälkeen pakka on tallennettu Flashcard-luokkaan. Käyttöjärjestelmä voi sitten käyttää pakkaa erilaisilla komennoilla, kuten ottamalla pakasta seuraavan kortin ```get_next_card()```-komennolla tai pyytämällä pakan sekoittamista komennolla ```generate_pack_random_order()```