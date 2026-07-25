# Elections Scraper

## Popis projektu:

Program stahuje výsledky českých parlamentních voleb z roku 2017 publikovaných na webu https://volby.gov.cz/pls/ps2017nss/ps3?xjazyk=CZ a ukládá je do CSV souboru.

## Instalace knihoven:

Pro správný běh kódu nejprve nainstalujte potřebné knihovny.
Ty, které jsou v projektu použity, jsou uloženy v souboru *requirements.txt*. 

Pro jejich instalaci doporučuji použít nové virtuální prostředí a spustit je pomocí příkazu:
``
pip install -r requirements.txt
``

## Spuštění projektu:

Spuštění souboru main.py v rámci příkazového řádku vyžaduje zadání dvou povinných argumentů.

*python main.py <odkaz_uzemniho_celku> <vysledny_soubor>*

Argumenty zadávejte vždy v následujícím pořadí:
1. argument: <odkaz_uzemniho_celku>
2. argument: <vysledny_soubor>

Následně se vám stáhnou výsledky jako soubor s příponou csv.

## Ukázka projektu:

#### Výsledky pro okres Jičín:
1. argument: ``"https://volby.gov.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=8&xnumnuts=5202"``
2. argument: ``"vysledky_jicin.csv"``

#### Spuštění programu:
``
python main.py "https://volby.gov.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=8&xnumnuts=5202" "vysledky_jicin.csv"
``

#### Průběh stahování:

``Ověřuji platnost URL: https://volby.gov.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=8&xnumnuts=5202 pro výstupní soubor: vysledky_jicin.csv``

``Stahuji data ze zadaného URL: https://volby.gov.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=8&xnumnuts=5202``

``Ukládám výsledky do výstupního souboru vysledky_jicin.csv``

``Ukončuji Elections Scraper.``

#### Výstup:

Součástí repozitáře je ukázkový CSV soubor *vysledky_jicin.csv*.










