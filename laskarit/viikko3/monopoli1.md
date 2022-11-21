```mermaid
  classDiagram
        Monopoli "1" -- "2" Noppa
        Monopoli "1" -- "2..8" Pelaaja
        Monopoli "1" -- "1" Pelilauta
        Pelilauta "1" -- "40" Ruutu
        Pelaaja "1" -- "1" Pelinappula
        Pelilauta "1" -- "2..8" Pelinappula

        class Ruutu {
                seuraava
        }

        
```