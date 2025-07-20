# Scorecard

**Scorecard** on sovellus, jolla voit kirjata piha- ja lautapelien tms. tuloksia
ylös. Onko yatzy-pelistäsi tuloslaput loppu? Eikö kesämökiltä löytynytkään
mölkkyä varten kynää ja paperia? Käytä scorecardia!

## Toiminnot

- [x] Käyttäjä voi luoda käyttäjätunnuksen ja kirjautumaan sisään sovellukseen
- [x] Käyttäjä voi luoda uuden tuloskortin ja kirjata siihen tuloksia
- [ ] Tuloskortti kertoo, kuka johtaa / on voittanut pelin
- [ ] Kirjautunut käyttäjä voi nähdä listan omista tuloskorteistaan
- [ ] Käyttäjä voi muokata tuloskorttiin kirjattuja tuloksia
- [ ] Kaksi eri käyttäjää voi muokata samaa tuloskorttia yhtä aikaa

## Asentaminen

Hae scorecardin lähdekoodi ja siirry kansioon
```shell
$ git clone git@github.com:JanneSalokoski/scorecard.git
$ cd scorecard
```

Asenna tarvittavat paketit (`Flask` ja `python-dotenv`)
```shell
$ pip install -f requirements.txt
```

Alusta tietokanta suorittamalla
```shell
$ flask --app app:create_app init-db
```

Käynnistä sovellus
```shell
$ flask run
```
tai `flask run --debug`

Scorecard on nyt käytössä osoitteessa [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Tausta

Sovellus on tehty Helsingin yliopiston tietojenkäsittelytieteen _Tietokannat ja
web-ohjelmointi_-kurssille. Siksi se on toteutettu [Flask](https://flask.palletsprojects.com/en/stable/)illa, eikä se hyödynnä javascriptia lainkaan.
