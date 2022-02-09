import datetime
import sys

class TIEDOT():
    paiva = ""
    maara = 0

class TARKAT():
    pienin = 0
    pieninpaiva = ""
    suurin = 0
    suurinpaiva = ""
    yht = 0
    ka = 0
    alku = ""
    loppu = ""

def valikko():
    print("Mitä haluat tehdä:\n1) Lue kuormatiedot\n2) Analysoi kuormatiedot")
    print("3) Tallenna kuormien tulostiedot\n4) Analysoi viikonpäivittäin")
    print("5) Analysoi kumulatiivisesti tiedostoon\n6) Analysoi kumulatiivisesti näytölle\n0) Lopeta")
    valinta = input("Valintasi: ")
    return valinta

def lue(): 
    tiedosto = input("Anna kuormatietotiedoston nimi: ")
    try:
        lue = open(tiedosto, 'r')
        lue.readline() #otsikkorivi
        tietolista = []
        
        while True:
            rivi = lue.readline()
            if len(rivi) == 0:
                break
            lista = rivi.split(";")
            
            paivam = datetime.datetime.strptime(lista[0] + lista[1], "%d.%m.%Y%H:%M:%S")
            kuorma = int(lista[2])
            olio = TIEDOT()
            olio.paiva = paivam
            olio.maara = kuorma
            tietolista.append(olio)
            
        print("Tiedosto '{0}' luettu, {1} riviä.\n".format(tiedosto, len(tietolista)))
        lue.close()
        
    except Exception:
        print("Tiedoston '{0}' käsittelyssä virhe, lopetetaan.".format(tiedosto))
        sys.exit(0)
        
    return tietolista

# pienin, suurin, näiden aikaväli, yht, k-a, lasketaan listan ensimmäinen ja viimeinen päivä
def analysoitied(tietolista):
    if len(tietolista) == 0:
        print("Lista on tyhjä. Lue ensin tiedosto.\n")
        return None
    
    yht = 0
    pie = tietolista[0].maara
    piepaiva = tietolista[0].paiva
    suur = tietolista[0].maara
    suurpaiva = tietolista[0].paiva
    alkpaiva = tietolista[0].paiva
    loppaiva = tietolista[0].paiva

    for alkio in tietolista: #pienin arvo ja päivä sekä suurin arvo ja päivä
        arvo = alkio.maara
        arvopaiva = alkio.paiva  
        yht = yht + arvo
        if pie > arvo:
            pie = arvo 
            piepaiva = arvopaiva
        elif pie == arvo and piepaiva > arvopaiva:
            piepaiva = arvopaiva                
        elif suur < arvo:
            suur = arvo
            suurpaiva = arvopaiva
        elif suur == arvo and suurpaiva > arvopaiva:
            suurpaiva = arvopaiva
                
        if alkpaiva > arvopaiva: #aloitus ja lopetus
            alkpaiva = arvopaiva
        elif loppaiva < arvopaiva:
            loppaiva = arvopaiva
    ka = yht / len(tietolista)
    
    arvot = TARKAT()
    arvot.pienin = pie
    arvot.pieninpaiva = piepaiva
    arvot.suurin = suur
    arvot.suurinpaiva = suurpaiva
    arvot.yht = yht
    arvot.ka = ka
    arvot.alku = alkpaiva
    arvot.loppu = loppaiva
    
    alku = alkpaiva.strftime("%d.%m.%Y")
    loppu = loppaiva.strftime("%d.%m.%Y")
    print("Data analysoitu ajalta {0} - {1}.\n".format(alku, loppu))
    return arvot

def tallennatied(arvot):
    if arvot == None:
        print("Ei tuloksia. Analysoi data ennen tallennusta.\n")
        return None

    tiedosto = input("Anna tulostiedoston nimi: ")
    try:
        kirj = open(tiedosto, 'w')
        pieninpaiva = arvot.pieninpaiva.strftime("%d.%m.%Y")
        suurinpaiva = arvot.suurinpaiva.strftime("%d.%m.%Y")
        ero = abs(arvot.pieninpaiva - arvot.suurinpaiva)
        rivi1 = "Pienin jätekuorma tuli {0} ja oli {1} kg.".format(pieninpaiva, arvot.pienin)
        rivi2 = "Suurin jätekuorma tuli {0} ja oli {1} kg.".format(suurinpaiva, arvot.suurin)
        rivi3 = "Pienimmän ja suurimman kuorman toimitusten välissä oli {0} päivää.".format(ero.days)
        rivi4 = "Analyysijaksolla jätettä tuli yhteensä {0} kg.".format(arvot.yht)
        rivi5 = "Keskimäärin jätekuorma oli {0} kg.".format(int(arvot.ka))
        print(rivi1 + "\n" + rivi2 + "\n" + rivi3 + "\n" +rivi4 + "\n" +rivi5)
        kirj.write(rivi1 + "\n" + rivi2 + "\n" + rivi3 + "\n" + rivi4 + "\n" + rivi5 + "\n")
        print("Tulokset tallennettu tiedostoon '{0}'.\n".format(tiedosto))    
        kirj.close()

    except Exception:
        print("Tiedoston käsittelyssä virhe, lopetetaan.")
        sys.exit(0)
    return None

def paivatied(tietolista):
    if len(tietolista) == 0:
        print("Lista on tyhjä. Lue ensin tiedosto.\n")
        return None
    
    lista = []
    viikko = ["Maanantai", "Tiistai", "Keskiviikko", "Torstai", "Perjantai", "Lauantai", "Sunnuntai"]
    for i in range(0,7):
        lista.append(0)
    for alkio in tietolista:
        paivnum = int(alkio.paiva.strftime("%w"))#%w eli 0 on sunnuntai 6 on lauantai
        lista[paivnum] = lista[paivnum] + alkio.maara
    print("Eri viikonpäivinä tuli seuraavat määrät jätettä:")
    
    for i in range(0, len(viikko)):
        if i == 6:
            print("{0};{1}\n".format(viikko[i], lista[0]))
            continue
        print("{0};{1}".format(viikko[i], lista[i + 1]))
    return None

def kumulatiiv(tietolista, arvot):#%j antaa vuosien päivät numeroina
    #lisätään listapaiva:an kaikki alotuksen ja lopetuksen väliset arvot timedelta:lla
    if arvot == None:
        print("Ei tuloksia. Analysoi data ennen tallennusta.\n")
        return None

    if len(tietolista) == 0:
        print("Lista on tyhjä. Lue ensin tiedosto.\n")
        return None
    
    lista = []
    listapaiva = []
    kumula = []
    aloitus = int(arvot.alku.strftime("%j"))
    lopetus = int(arvot.loppu.strftime("%j"))
    paiva = arvot.alku
    yht = 0
    kumula.append("Jätettä kertyi vuoden aikana päivittäin seuraavalla tavalla:")
    
    for i in range(0,366): # lisätään jokaiselle päivälle 0, jotta voidaan käyttää mitä tahansa päivää halutaan
        lista.append(0)
        listapaiva.append(0)
    for alkio in tietolista:
        vpaiva = int(alkio.paiva.strftime("%j"))# vuoden ensimmäinen päivä on 001 viimeinen 366
        lista[vpaiva] += alkio.maara
        
    for i in range(aloitus,lopetus + 1): #lisätään jokaiselle päivälle päivämäärä ja kumulatiivinen summa
        yht += lista[i]
        listapaiva[i] = paiva.strftime("%d.%m.%Y")
        paiva = paiva + datetime.timedelta(days=+1)        
        kumula.append("{0};{1}".format(listapaiva[i] ,yht))
    return kumula

def tiedtall(kumula):
    if kumula == None:
        return None
    
    try:
        tiedosto = open("kumulatiivinen.txt", 'w')
        for i in range(len(kumula)):
            tiedosto.write(kumula[i]+ "\n")
        print("Tiedosto 'kumulatiivinen.txt' tallennettu.\n")
        tiedosto.close()        
            
    except Exception:
        print("Tiedoston 'kumulatiivinen.txt' käsittelyssä virhe, lopetetaan.")
        sys.exit(0)
    return None

def tiednaytto(kumula):
    if kumula == None:
        return None
        
    for i in range(len(kumula)):
        print(kumula[i])
    print()
    return None
