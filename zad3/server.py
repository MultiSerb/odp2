from FizickoLice import FizickoLice
import socket,pickle,hashlib
from Korisnik import Korisnik

def hesiranje(tekst):
    return hashlib.sha256(tekst.encode()).hexdigest()
def log_info(tekst):
    f = open('log.txt','a')
    f.write(tekst+'\n')
    f.close()
def cuvanje_replikacije(lica):
    f = open('lica.txt','a')
    for lice in lica.values():
        f.write(str(lice)+'\n')
    f.close()

def ucitaj_korisnike():
    f=open("korisnici.txt")
    linije=f.readlines()
    for linija in linije:
        username = linija.split(' ')[0]
        privilages = linija.split(' ')[1]
        password = linija.split(' ')[2]
        korisnik = Korisnik(username,privilages,hesiranje(password))
        korisnici[korisnik.username]=korisnik
        
stanje = ""
korisnik=None
lica={

}
korisnici={

}
def logovanje(korisnik):
    if (korisnik.username in korisnici.keys()) and (hesiranje(korisnik.password) == korisnici[korisnik.username].password ):
        
        korisnici[korisnik.username].auth=True
       
    return korisnici[korisnik.username]

def dodaj_lice(lice):
    if lice.jmbg not in lica.keys():
        lica[lice.jmbg]=lice
        return f"Lice sa jmbg-om:{lice.jmbg} uspesno dodato"
    else:
        return f"Lice sa datim jmbg-om je vec u recniku!"
def izmeni_lice(lice):
    if lice.jmbg in lica.keys():
        lica[lice.jmbg]=lice
        return f"Uspesno izmenjeno lice sa jmbg-om:{lice.jmbg}"
    else:
        return f"Greska ne postoji lice sa datim jmbg-om"
def lice_citanje(jmbg):
    if jmbg in lica.keys():
        return lica[jmbg].__str__()
    else:
        return "Ne postoji lice sa datim jmbg-om"
def lice_brisanje(jmbg):
    if jmbg in lica.keys():
        lica.pop(jmbg)
        
        return f"Uspesno obrisano lice sa jmbg-om:{jmbg}"
    else:
        return f"Greska ne postoji lice sa datim jmbg-om"

ucitaj_korisnike()

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('localhost',7000))
server.listen()

print("Server is listening...")
kanal,adresa=server.accept()
print("server uspesno uspostavio vezu sa monitorom...")
stanje=kanal.recv(1024).decode()
print(stanje)
kanal.send(stanje.encode())
kanal.close()
print("Zatvaranje veze sa monitorom...")
kanal,adresa = server.accept()
print("Server prihvatio vezu sa klijentom...")
while True:
    
    korisnik = pickle.loads(kanal.recv(1024))
    
    korisnik=logovanje(korisnik)
    print("Ulogovan")
    kanal.send(pickle.dumps(korisnik))
    if korisnik.auth:break

print("Izasao iz orve while petlje..")
while True:
    
    opcija = kanal.recv(1024).decode()
    if not opcija:break
    if opcija == "ADD":
        if 'ADD' in korisnik.privilages:
            lice=pickle.loads(kanal.recv(1024))
            odgovor=dodaj_lice(lice)
            log_info(odgovor)
        else:
            odgovor="Nemate prava da izvrsite ovu operaciju!"
    if opcija == "CHANGE":
        if 'EDIT' in korisnik.privilages:
            lice=pickle.loads(kanal.recv(1024))
            odgovor = izmeni_lice(lice)
            log_info(odgovor)

        else:
            odgovor="Nemate prava da izvrsite ovu operaciju!"
    if opcija == "READ":
        if 'READALL' in korisnik.privilages:
            jmbg = kanal.recv(1024).decode()
            odgovor = lice_citanje(jmbg)

        else:
            odgovor="Nemate prava da izvrsite ovu operaciju!"
    if opcija == "DELETE":
        if 'EDIT' in korisnik.privilages:
        
            jmbg = kanal.recv(1024).decode()
            odgovor=lice_brisanje(jmbg)
            log_info(odgovor)

        else:
            odgovor="Nemate prava da izvrsite ovu operaciju!"
    if opcija == "READALL":
            if 'READALL' in korisnik.privilages:
                kanal.send(pickle.dumps(lica))
                odgovor="Uspesno procitana lica"
            else:
                odgovor = "Nemate prava da izvrsite ovu operaciju!"
        
    if opcija == "WRITE_ALL":
        lica=pickle.loads(kanal.recv(1024))
        odgovor = "Uspesno replicirana lica!"
        print(lica)
        cuvanje_replikacije(lica)
    if opcija == "GET_STATE":
        odgovor=stanje
    if opcija == "SET_STATE":
        print("dobijeno set_state")
        stanje=kanal.recv(1024).decode()
        print(f"Novo stanje servera:{stanje}")
        odgovor = f"Uspesno postavljeno stanje na:{stanje}"


    
    kanal.send(odgovor.encode())
kanal.close()
