from bs4 import BeautifulSoup
import requests
import re
import json
import os
import skrapado.konstantoj as konst


class BonalingvoSkrapado(BeautifulSoup):
    def __init__(self):
        self.peto = requests.get(konst.BASA_LIGILO).text
        super(BonalingvoSkrapado, self).__init__(self.peto, "lxml")
        self.kolektataj_datumoj = []

    def kolektu_vortajn_datumojn(self):
        vortujo = self.find("div", {"id": "tuta"}).dl
        krudaj_vortaj_nomoj = vortujo.find_all("dt")
        vortaj_enhavoj = vortujo.find_all("dd")

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
            self.kolektataj_datumoj.append(rezulta_skrapado)

    def kreu_dosieron_json(self):
        datumoj_json = json.dumps(self.kolektataj_datumoj, indent=2, ensure_ascii=False)
        vojo = os.getcwd()
        kunigita_vojo = os.path.join(vojo, konst.DOSIERUJO)
        if not os.path.exists(kunigita_vojo):
            os.mkdir(kunigita_vojo)

        with open(os.path.join(kunigita_vojo, "bonalingvo.json"), "w", encoding="utf8") as dosiero:
            dosiero.write(datumoj_json)

        print("Skrapado finita.")
