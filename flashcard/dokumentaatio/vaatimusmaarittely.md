# Vaatimusmäärittely

## Tarkoitus
Sovelluksen avulla käyttäjän pitäisi pystyä luomaan, hallitsemaan ja tarkastelemaan ns. suomi-japani "flashcard"-kortteja graafisessa käyttöliittymässä.

## Käyttöliittymä
Käyttäjän pitäisi pystyä navigoimaan käyttöliittymää ja käyttämään kortteja vaikka ei ymmärtäisi sanaakaan japania, vaikkakin itse kortit olisivatkin tällaisessa tilanteessa epäkäytännöllisiä.

#### Sovelluksen aloitus
![](./img/alku.png)

#### Korttien tarkastelu
![](./img/tarkastelu.png)

#### Asetukset (Avautuu uuteen ikkunaan?)
![](./img/asetukset.png)

## Toiminnallisuus

### Perusversio
- Käyttöliittymä korttien lukemiseen
    - Kortti antaa lauseen japaniksi, josta yksi sana on alleviivattu
    - Kortin "kääntöpuolella" löytyy esim. lukutapa ja suomen kielen vastine sanalle
- Korttien lataus xml-tiedostosta
- Korttien avaaminen joko ohjelman alihakemistosta tai valinnaisesta osoitteesta

### Muuta lisättävää jne.
- Korttien muokkaus, luonti ja poisto graafisen käyttöliittymän avulla
- Käyttäjä voi kirjoittaa alleviivatun sanan lukutavan, jonka sovellus sitten toteaa oikeaksi tai vääräksi.
-

## .xmlpack tiedoston esimerkki
```
<pack>
    <name></name>
    <desc></desc>

    <cards>
        <card>
            <!-- Etsittävä sana ympäröity **-merkeillä -->
            <sentence>This is a **sentence**.</sentence>
            <reading></reading>
            <translation></translation>
        </card>
    </cards>
</pack>
```