import socket, pickle

stanje = ""

lekovi = {}

def log_info(message):
    # Log
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
    log_info(odgovor)
    return odgovor.encode()

def izmeni_lek(poruka):
    lek = pickle.loads(poruka)
    if lek.id not in lekovi:
        odgovor = f"Lek sa id-em: {lek.id} ne postoji u bazi!"
    else:
        lekovi[lek.id] = lek
        odgovor = f"Lek sa id-em: {lek.id} uspesno izmenjen."
    log_info(odgovor)
    return odgovor.encode()
    
def izbrisi_lek(id):
    if id not in lekovi:
        odgovor = f"Lek sa id-em: {id} ne postoji u bazi!"
    else:
        del lekovi[id]
        odgovor = f"Lek sa id-em: {id} uspesno obrisan."
    log_info(odgovor)
    return odgovor.encode()

def procitaj_lek(id):
    if id not in lekovi:
        odgovor = f"Lek sa id-em: {id} ne postoji u bazi!"
        log_info(odgovor)
        return odgovor.encode()
    else:
        odgovor = pickle.dumps(lekovi[id])
        return odgovor

def main():
    global lekovi
    global stanje

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 6000))
    server.listen()
    print("Server je pokrenut.")

    kanal, adresa = server.accept()
    print(f"Prihvacena je konekcija monitora sa adrese: {adresa}")

    stanje = kanal.recv(1024).decode()
    print(f"Novo stanje: {stanje}")
    kanal.send(("Stanje uspesno azurirano!".encode()))
    kanal.close()

    kanal, adresa = server.accept()
    print(f"Prihvacena je konekcija klijenta sa adrese: {adresa}")

    while True: 
        try:
            opcija = kanal.recv(1024).decode()
        except Exception as ex:
            print(ex)
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

    
