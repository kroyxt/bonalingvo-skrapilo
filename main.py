from skrapado.skrapado import BonalingvoSkrapado


if __name__ == "__main__":
    skrapado = BonalingvoSkrapado()
    skrapado.kolektu_vortajn_datumojn()
    skrapado.kreu_dosieron_json()
