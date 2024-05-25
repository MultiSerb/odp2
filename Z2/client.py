import socket, pickle
from datetime import date
from lek import Lek

def pokupi_informacije_leka_za_slanje():
    id = input("ID leka -> ")
    naziv = input("Naziv leka -> ")
    lek = Lek(id, naziv)
    return pickle.dumps(lek)

def pokupi_informaciju_id_leka_za_slanje():
    return input("ID leka -> ").encode()

def iscitaj_lek(odgovor):
    try:
        lek = pickle.loads(odgovor)
        print(lek)
    except:
        print(odgovor.decode())

def main():
    klijentM = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    klijentM.connect(('localhost', 3000))
    print("Veza sa monitorom je uspostavljena.")
    portovi = klijentM.recv(1024).decode().split(',')
    print(f"Portovi primarnog i sekundarnog servera su: {portovi}.")
    print("Zatvaranje konekcije sa monitorom.")
    klijentM.close()

    try:
        klijentP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        klijentP.connect(('localhost', int(portovi[0])))
        print("Veza sa primarnim serverom je uspostavljena.")
    except Exception as ex:
        print(ex)

    try:
        klijentS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        klijentS.connect(('localhost', int(portovi[1])))
        print("Veza sa sekundarnim serverom je uspostavljena.")
    except Exception as ex:
        print(ex)

    while True:             
        operacija = input("Odaberite operaciju: \n1.Dodaj lek \n2.Izmeni lek \n3.Obrisi lek\n4.Procitaj lek\n5.Repliciraj podatke\n") 
        if not operacija : break         
        if operacija == "1": # Dodaj lek
            try:   
                klijentP.send(("ADD").encode())  
                klijentP.send(pokupi_informacije_leka_za_slanje())
                print(klijentP.recv(1024).decode())
            except Exception as ex:
                print(ex)
        elif operacija == "2": # Izmeni lek 
            try:   
                klijentP.send(("UPDATE").encode())
                klijentP.send(pokupi_informacije_leka_za_slanje())
                print(klijentP.recv(1024).decode())
            except Exception as ex:
                print(ex)
        elif operacija == "3": # Obrisi lek
            try: 
                klijentP.send(("DELETE").encode())
                klijentP.send(pokupi_informaciju_id_leka_za_slanje())
                print(klijentP.recv(1024).decode())
            except Exception as ex:
                print(ex)     
        elif operacija == "4": # Procitaj lek 
            try:
                klijentP.send(("READ").encode())
                klijentP.send(pokupi_informaciju_id_leka_za_slanje())
                iscitaj_lek(klijentP.recv(1024))
            except Exception as ex:
                print(ex)
        elif operacija == "5": # Replikacija 
            try:
                klijentP.send(("READ_ALL").encode())
                klijentS.send(("WRITE_ALL").encode())
                klijentS.send(klijentP.recv(1024))

                print(klijentP.recv(1024).decode())
                print(klijentS.recv(1024).decode()) 
            except Exception as ex:
                print(ex)
        else:
            print("Molimo unesite validnu operaciju.")
            continue

    klijentP.close() 
    klijentS.close()
    print("Zatvaranje konekcije.")
    
main()