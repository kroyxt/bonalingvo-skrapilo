from bs4 import BeautifulSoup
import requests
import re
import json


# Kolektu la enhavon de la retpaĝo
bona_lingvo_ligilo = "https://bonalingvo.info/ricerca.php?tuta=1"
bona_lingvo_enhavo = requests.get(bona_lingvo_ligilo).text
soup = BeautifulSoup(bona_lingvo_enhavo, "lxml")

# Trovu la ujon kiu enhavas la datumojn
vortujo = soup.find("div", {"id": "tuta"}).dl

# Kolektu la nomon de ĉiu vorto kaj sian enhavon
vortaj_nomoj = vortujo.find_all("dt")
vortaj_enhavoj = vortujo.find_all("dd")

# Kreu malplenan tabulan variablon kiu havos la rezulton de la skrapado
kolektitaj_datumoj = []

for indekso, vorto in enumerate(vortaj_nomoj):
    _vorto = vorto.text.replace(":", "").strip().split(" ")
    vorta_nomo = _vorto[0]
    morfologio = _vorto[1]
    aldono = _vorto[2] if len(_vorto) > 2 else ""
    rezulto = {
        "vorto": vorta_nomo,
        "morfologio": re.sub(r"[()]", "", morfologio),
        "aldono": re.sub(r"[\[\]]", "", aldono),
        "enhavo": vortaj_enhavoj[indekso].text.strip()
    }
    kolektitaj_datumoj.append(rezulto)

# Kodifu la datumon kolektitan al dosieron Json
dosiero_json = json.dumps(kolektitaj_datumoj, indent=2, ensure_ascii=False)

# Kreu la dosieron Json
with open("bonalingvo.json", "w", encoding="utf8") as dosiero:
    dosiero.write(dosiero_json)
