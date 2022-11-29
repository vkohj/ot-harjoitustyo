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



