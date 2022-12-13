## Viikon 3 muutokset
2022.11.16 - 2022.11.22

* Luotiin ohjelman runko
    * Lisättiin komentorivi käyttöliittymä ohjelmalle sen kehittämistä varten
    * FileReader-luokka, joka pystyy tarkastelemaan ja lukemaan .xmlpack-tiedostoja
    * Flashcard-luokka, joka yhdistää komentorivin ja FileReader-luokan
    * Luokat korteille ja korttipakoille
* Käyttäjä pystyy valitsemaan /kortit/ kansiossa olevan korttipakan ja näkemään sen kortit listana
* Testit
    * Lisättiin testit FileReader-luokalle (100% coverage)
* Lisättiin tasks.py-tiedosto, jota voi käyttää invoke moduulin avulla

## Viikon 4 muutokset
2022.11.23 - 2022.11.29

* Konsolikäyttöliittymän uudistuksia
    * Muutettiin päävalikko korttipakan lataamisruuduksi
    * Korttien opettelu satunnaisessa järjestyksessä
    * Korttien muokkausvalikko
    * Tallennuksen varmistusvalikko
    * Pientä refraktorointia
* Ohjelmistotoimintojen uudistuksia
    * Kortit voidaan nyt sekoittaa eri järjestykseen
    * Kortien tietoja voidaan muokata
    * Uusien korttien luonti
    * Tallennus .xmlpack tiedostoon
    * Pakkan muuttujat "path" ja "unsaved_changes"
    * Pientä refraktorointia
* Testit
    * Uudet testit FileReader-luokalle
        * Tiedostojen tallentaminen
    * Testit Pack- ja Card-luokalle
    * Joitain testejä Flashcard-luokalle
* Lisättiin pylintin käyttö tasks.py -tiedostoon

## Viikon 5 muutokset
2022.11.30 - 2022.12.06

* Graafinen käyttöliittymä
    * Tkinter käyttöliittymävaihtoehto
    * Korttien avaaminen ja opiskelutoiminnallisuus
* Vaihdettiin graafinen käyttöliittymä pääkäyttöliittymäksi
    * Konsolikäyttöliittymän voi avata  ```--console``` argumentilla tai komennolla ```poetry run invoke console```

## Viikon 5 muutokset
2022.12.07 - 2022.12.13

* Graafinen käyttöliittymä
    * Asetusikkuna ja ylävalikko
    * Fonttikoon ja fontin perheen muutos
    * Ikkunalle annettiin minsize- ja maxsize-arvot
* TkinterGUI
    * Asetusten hallinnointi
    * Valikoiden uudelleenluominen
* Flashcard
    * Asetustiedoston "setting.xml" lataaminen ja tallentaminen
* Filereader
    * Simppeleiden .xml-tiedostojen luku sanakirjaan
    * Sanakirjan tallentaminen .xml-tiedostoon
* Yleisiä bugikorjauksia
* Dokumentaatio
    * Muutoksia arkkitehtuuri-tiedostoon
    * Lisättiin ohjelman käyttöohje tiedostoon ohje.md
    * Lisättiin DOCSTRING-dokumentaatio luokkiin Flashcard, Card, Pack, TkinterGUI ja Console


