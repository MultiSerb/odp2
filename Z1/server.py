import socket, pickle
from direktorijum_korisnika import *

def autentifikuj_korisnika(kanal):
    global trenutni_korisnik
    korisnicko_ime = kanal.recv(1024).decode()
    lozinka = kanal.recv(1024).decode()
    if autentifikacija(korisnicko_ime, lozinka):
        kanal.send(("Uspesna autentifikacija!").encode())
        trenutni_korisnik = korisnici[korisnicko_ime]
        return True
    else:
        kanal.send(("Neuspesna autentifikacija!").encode())
        return False

lekovi = {}

def log_info(message):
    log = open("log.txt", "a")
    log.write(message + "\n")
    log.close()

def dodaj_lek(poruka):
    lek = pickle.loads(poruka)
    if lek.id in lekovi:
        odgovor = f"Lek sa id-em: {lek.id} vec postoji u bazi!"
    else:
        lekovi[lek.id] = lek
        odgovor = f"Lek sa id-em: {lek.id} uspesno upisan u bazu."
    print(odgovor)
    log_info(odgovor)
    return odgovor.encode()

def izmeni_lek(poruka):
    lek = pickle.loads(poruka)
    if lek.id not in lekovi:
        odgovor = f"Lek sa id-em: {lek.id} ne postoji u bazi!"
    else:
        lekovi[lek.id] = lek
        odgovor = f"Lek sa id-em: {lek.id} uspesno izmenjen."
    print(odgovor)
    log_info(odgovor)
    return odgovor.encode()
    
def izbrisi_lek(id):
    if id not in lekovi:
        odgovor = f"Lek sa id-em: {id} ne postoji u bazi!"
    else:
        del lekovi[id]
        odgovor = f"Lek sa id-em: {id} uspesno obrisan."
    print(odgovor)
    log_info(odgovor)
    return odgovor.encode()

def procitaj_lek(id):
    if id not in lekovi:
        odgovor = f"Lek sa id-em: {id} ne postoji u bazi!"
        print(odgovor)
        log_info(odgovor)
        return odgovor.encode()
    else:
        print(f"Uspesno procitan lek sa id-em: {id}.")
        odgovor = pickle.dumps(lekovi[id])
        return odgovor

def main():
    global lekovi

    dodaj_korisnika("test", "test")
    dodaj_korisnika("pera", "p3r@")
    dodaj_korisnika("admin", "Adm1n")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 7000))
    server.listen()
    print("Server je pokrenut.")

    kanal, adresa = server.accept()
    print(f"Prihvacena je konekcija sa adrese: {adresa}")

    while not autentifikuj_korisnika(kanal):
        autentifikuj_korisnika(kanal)

    while True: 
        opcija = kanal.recv(1024).decode()
        if not opcija : break
        if opcija == "ADD": # Dodaj lek
            odgovor = dodaj_lek(kanal.recv(1024))
        elif opcija == "UPDATE": # Izmeni lek
            odgovor = izmeni_lek(kanal.recv(1024))
        elif opcija == "DELETE": # Obrisi lek
            odgovor = izbrisi_lek(kanal.recv(1024).decode())
        elif opcija == "READ": # Procitaj lek
            odgovor = procitaj_lek(kanal.recv(1024).decode())            
        elif opcija == "READ_ALL": # Pročitaj sve za replikaciju
            kanal.send(pickle.dumps(lekovi))
            odgovor = ("Uspesno procitani svi podaci!").encode()           
        elif opcija == "WRITE_ALL": # Pročitaj sve za replikaciju
            lekovi = pickle.loads(kanal.recv(1024))
            odgovor = ("Uspesno upisani svi podaci!").encode()          

            print("Replicirano:")
            for l in lekovi.values(): print(l) 
        try:
            kanal.send(odgovor)
        except Exception as ex:
            print(ex)
    
    print("Server se gasi.")
    server.close()


main()

    
