# Suomi-japani Flashcard-sovellus
Ohjelma on keskeneräinen ja osa [Helsingin Yliopiston ohjelmistotekniikan](https://ohjelmistotekniikka-hy.github.io/) kurssia.

Sovellus tulee mahdollistamaan suomi-japani korttipakkojen luomisen, muokkaamisen ja tarkastelemisen. Kortteja tarkastellessa käyttäjä näkee ensin japaninkielisen lauseen ja erikseen eritellyn sanan alleviivattuna. Painamalla nappia käyttäjä saa näkyviin sanan lukutavan ja suomen kielen käännöksen.


## Uusin julkaistu versio
[Flashcard - Loppupalautus](https://github.com/vkohj/ot-harjoitustyo/releases/tag/loppupalautus)

## Vaatimukset
⚠️ Python 3.8 tai uudempi ⚠️

Sovellus suositellaan asentamaan poetry-järjestelmällä.


### Poetryn kautta automaattisesti asennettavat moduulit
* Invoke 1.7.3 tai uudempi
* Pytest 7.2.0 tai uudempi (dev)
* Coverage 6.5.0 tai uudempi (dev)
* pylint 2.15.6 tai uudempi (dev)
* autopep8 2.0.0 tai uudempi (dev)

## Asennus
⚠️ Huomaathan, että alla olevat komennot suoritetaan ohjelman pääkansiossa "flashcard"!

Ohjelman voi asentaa joko ilman tai sisältäen ohjelman kehitykseen vaadittavat moduulit.

* Käyttäjälle: ```poetry install --without dev```
* Ohjelmoijalle: ```poetry install```

## Käynnistäminen

### Graafinen käyttöliittymä
* Linux: ```poetry run invoke start```
* Windows: Käynnistä ```start.bat```
* Vaihtoehtoinen: ```poetry run python src``` (Windows, Linux yms.)

### Konsolikäyttöliittymä
* Linux: ```poetry run invoke console```
* Vaihtoehtoinen: ```poetry run python src --console``` (Windows, Linux yms.)

## Dokumentaatio
* [Changelog](./flashcard/dokumentaatio/changelog.md)
* [Vaatimusmäärittely](./flashcard/dokumentaatio/vaatimusmaarittely.md)
* [Arkkitehtuuri](./flashcard/dokumentaatio/arkkitehtuuri.md)
* [Työaikakirjanpito](./flashcard/dokumentaatio/tuntikirjanpito.md)

## Lisäkomentoja (kehittämisversiolle)
Projekti sisältää myös muutaman ylimääräisen invoke-komennon. Nämä komennot vaativat, että olet asentanut ohjelman kehittämisversion (katso kohdasta "Asennus")

* Testien suorittaminen:
```poetry run invoke test```
* Testien kattaavuus ja sen tulostus html-tiedostoon
```poetry run invoke coverage-report```
* Ohjelmakoodin laaduntarkastus
```poetry run invoke lint```

