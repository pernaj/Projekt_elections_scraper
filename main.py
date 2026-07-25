import sys
import csv

from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup as bs
from bs4.element import Tag

def get_parsed_html(url: str) -> bs:
    '''Ověří dostupnost URL stránky, vrátí naparsovaný HTML obsah stránky.'''
    response = requests.get(url)
    if response.status_code != 200:
        sys.exit()
    else:
        return bs(response.text, features="html.parser")

def get_all_tags(parsed_html: bs, tag: str) -> list:
    '''Vrátí seznam všech HTML tagů zadaného typu z naparsovaného HTML obsahu.'''
    return parsed_html.find_all(tag)

def get_clean_number(tag: Tag) -> int:
    '''Odstraní oddělovače tisíců a převede text tagu na celé číslo.'''
    return int(tag.text.replace("\xa0", ""))

def get_participation_data(parsed_html: bs) -> dict[str, int]:
    '''
    Získá údaje o volební účasti. Vrátí slovník s počtem registrovaných voličů,
    vydaných obálek a platných hlasů.'''
    return {
        "registered": get_clean_number(
            parsed_html.find("td", headers="sa2")),
        "envelopes": get_clean_number(
            parsed_html.find("td", headers="sa3")),
        "valid":get_clean_number(
            parsed_html.find("td", headers="sa6"))
    }

def get_party_results(parsed_html: bs) -> dict[str, int]:
    '''
    Získá výsledky politických stran v územním celku. 
    Vrátí slovník ve formátu {název strany: počet hlasů}.'''
    party_results = {}
    for tr_tags in get_all_tags(parsed_html, "tr"):
        party = tr_tags.find("td", class_ = "overflow_name")
        if party is None:
            continue
                      
        tab1 = tr_tags.find("td", class_="cislo", headers="t1sa2 t1sb3")
        tab2 = tr_tags.find("td", class_="cislo", headers="t2sa2 t2sb3")
        votes = tab1 or tab2
        if votes is None:
            continue

        party_results[party.text.strip()] = get_clean_number(votes)
    return party_results

if len(sys.argv) != 3: # kontrola argumentů
    print("Nebyl zadán správný počet argumentů.", 
          "Zadejte URL a název výstupního souboru.", sep="\n")
    sys.exit()
else:
    district_url = sys.argv[1] 
    output_file = sys.argv[2]

print(f"Ověřuji platnost URL: {district_url} pro výstupní soubor: {output_file}")

ELECTIONS_URL = "https://volby.gov.cz/pls/ps2017nss/ps3?xjazyk=CZ"

elections_parsed_html = get_parsed_html(ELECTIONS_URL)

districts_dict = {}
for tr in get_all_tags(elections_parsed_html, "tr"):
    elections_td_tags = tr.find_all("td")

    if len(elections_td_tags) >= 4:
        district_name = elections_td_tags[1].text
        href = elections_td_tags[3].find("a")["href"]
        districts_dict[district_name] = urljoin(ELECTIONS_URL, href)

if district_url in districts_dict.values():
    print(f"Stahuji data ze zadaného URL: {district_url}")
else:
    print(f"Zadaný URL {district_url} není platnou doménou.",
          "Zadejte správný URL a název výstupního souboru.", sep="\n")
    sys.exit()

# všechny okresy mají stejnou strukturu html až na Zahraničí -> samostatná větev
if district_url == districts_dict.get("Zahraničí"):

    foreign_district_parsed_html = get_parsed_html(district_url)
 
    foreign_municipalities_list = [] 

    for tag in get_all_tags(foreign_district_parsed_html, "tr"):
        location_tag = tag.find("td", headers="s3")
        code_tag = tag.find("td", headers="s4")
        if location_tag is None or code_tag is None:
            continue
        location = location_tag.text.strip()
        code = code_tag.text.strip()
 
        link_tag = tag.find("td", headers="s4").find("a")
        if link_tag is None:
            continue
        link = link_tag["href"]

        foreign_municipality = {
            "code": code,
            "location": location,
            "link": urljoin(ELECTIONS_URL, link)
        }
        foreign_municipalities_list.append(foreign_municipality)

    results_list = []

    for foreign_municipality in foreign_municipalities_list:
        foreign_municipality_parsed_html = get_parsed_html(foreign_municipality["link"])
    
        results = {
            "code": foreign_municipality["code"],
            "location": foreign_municipality["location"]
        }

        results.update(get_participation_data(foreign_municipality_parsed_html))
        results.update(get_party_results(foreign_municipality_parsed_html))

        results_list.append(results)

else:   
    district_parsed_html = get_parsed_html(district_url)

    municipalities_list = []

    for tag in get_all_tags(district_parsed_html, "tr"):
        location = tag.find("td", class_="overflow_name")
        if location: 
            location_name = location.text.strip() 
        else: # některé obce nemají class "overflow_name" -> větev else
            td_tags = tag.find_all("td")
            if len(td_tags) >= 2:
                location_name = td_tags[1].text.strip()
            else:
                continue

        code = tag.find("td", class_="cislo")   
        if code is None:
            continue
   
        link_tag = tag.find("a")
        if link_tag is None:
            continue
        link = link_tag["href"]

        municipality = {
            "code": code.text.strip(),
            "location": location_name,
            "link": urljoin(ELECTIONS_URL, link)
        } 
        municipalities_list.append(municipality)

    results_list = []
    
    for municipality in municipalities_list:
        municipality_parsed_html = get_parsed_html(municipality["link"])           
        results = {
            "code": municipality["code"],
            "location": municipality["location"]
            }
            
        results.update(get_participation_data(municipality_parsed_html))
        results.update(get_party_results(municipality_parsed_html))
           
        results_list.append(results)
            
print(f"Ukládám výsledky do výstupního souboru {output_file}")

fieldnames = []

for row in results_list:
    for key in row.keys():
        if key not in fieldnames:
            fieldnames.append(key)
      
with open(output_file, 
          mode="w",
          encoding="UTF-8",
          newline="") as csv_file:
    writer = csv.DictWriter(
        csv_file, 
        fieldnames=fieldnames
    )
    writer.writeheader()
    writer.writerows(results_list)   

print("Ukončuji Elections Scraper.")


