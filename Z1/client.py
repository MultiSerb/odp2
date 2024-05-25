import socket, pickle
from lek import Lek

def login(klijent):
    korisnicko_ime = input("Unesite korisnicko ime -> ")
    lozinka = input("Unesite lozinku -> ")
    klijent.send(korisnicko_ime.encode())
    klijent.send(lozinka.encode())
    odgovor = klijent.recv(1024).decode()
    print(odgovor)
    return "Uspesna" in odgovor  

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
    klijentP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    klijentP.connect(('localhost', 6000))
    print("Veza sa primarnim serverom je uspostavljena.")

    while not login(klijentP):
        login(klijentP)

    klijentS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    klijentS.connect(('localhost', 7000))
    print("Veza sa sekundarnim serverom je uspostavljena.")

    while not login(klijentS):
        login(klijentS)

    while True: 
        operacija = input("Odaberite operaciju: \n1.Dodaj lek \n2.Izmeni lek \n3.Obrisi lek\n4.Procitaj lek\n5.Repliciraj podatke\n") 
        if not operacija : break         
        if operacija == "1": # Dodaj lek   
            klijentP.send(("ADD").encode())
            klijentP.send(pokupi_informacije_leka_za_slanje())
            print(klijentP.recv(1024).decode())
        elif operacija == "2": # Izmeni lek 
            klijentP.send(("UPDATE").encode())
            klijentP.send(pokupi_informacije_leka_za_slanje())
            print(klijentP.recv(1024).decode())
        elif operacija == "3": # Obrisi lek 
            klijentP.send(("DELETE").encode())
            klijentP.send(pokupi_informaciju_id_leka_za_slanje())
            print(klijentP.recv(1024).decode())     
        elif operacija == "4": # Procitaj lek 
            klijentP.send(("READ").encode()) 
            klijentP.send(pokupi_informaciju_id_leka_za_slanje())
            iscitaj_lek(klijentP.recv(1024))
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