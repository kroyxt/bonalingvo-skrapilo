from bs4 import BeautifulSoup
import requests
import re
import json
from skrapado.constants import BASA_LIGILO, ELIGA_VOJO


class BonalingvoSkrapado:
    def __init__(self):
        self.peto = requests.get(BASA_LIGILO).text
        self.soup = BeautifulSoup(self.peto, "lxml")

    def kolektu_vortajn_datumojn(self):
        vortujo = self.soup.find("div", {"id": "tuta"}).dl
        krudaj_vortaj_nomoj = vortujo.find_all("dt")
        vortaj_enhavoj = vortujo.find_all("dd")
        datumoj = []

        for indekso, vorto in enumerate(krudaj_vortaj_nomoj):
            krudaj_datumoj = vorto.text.replace(":", "").strip().split(" ")
            vorto = krudaj_datumoj[0]
            morfologio = krudaj_datumoj[1]
            aldono = krudaj_datumoj[2] if len(krudaj_datumoj) > 2 else ""
            enhavo = vortaj_enhavoj[indekso].text.strip()
            rezulta_skrapado = {
                "vorto": vorto,
                "morfologio": re.sub(r"[()]", "", morfologio),
                "aldono": re.sub(r"[\[\]]", "", aldono),
                "enhavo": enhavo
            }
            datumoj.append(rezulta_skrapado)

        return datumoj

    def kreu_dosieron_json(self, datumoj):
        datumoj_json = json.dumps(datumoj, indent=2, ensure_ascii=False)
        with open(ELIGA_VOJO, "w", encoding="utf8") as dosiero:
            dosiero.write(datumoj_json)
