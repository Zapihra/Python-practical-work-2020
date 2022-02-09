######################################################################
# CT60A0203 Ohjelmoinnin perusteet
# Tekijä: Iida Vaaja
# Opiskelijanumero: 606562
# Päivämäärä: 10.-16.11.
# Yhteistyö ja lähteet, nimi ja yhteistyön muoto:
# Lähde: opinto-opas, assarit
######################################################################

import harkkakirj2 as harkkakirj

def paaohjelma():
    tietolista = []
    kumula = []
    arvot = None
    while True:
        valinta = harkkakirj.valikko()
        if valinta == "1":
            tietolista = harkkakirj.lue()
        elif valinta == "2":
            arvot = harkkakirj.analysoitied(tietolista)
        elif valinta == "3":
            harkkakirj.tallennatied(arvot)
        elif valinta == "4":
            harkkakirj.paivatied(tietolista)
        elif valinta == "5":
            kumula = harkkakirj.kumulatiiv(tietolista, arvot)
            harkkakirj.tiedtall(kumula)
        elif valinta == "6":
            kumula = harkkakirj.kumulatiiv(tietolista, arvot)
            harkkakirj.tiednaytto(kumula)
        elif valinta == "0":
            print("Kiitos ohjelman käytöstä.")
            break
        else:
            print("Valintaa ei tunnistettu, yritä uudestaan.\n")
    return None

paaohjelma()
