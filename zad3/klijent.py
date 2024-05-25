import socket,pickle
from FizickoLice import FizickoLice
from Korisnik import Korisnik
def lice_za_slanje():
    jmbg=input("Unesite jmbg:")
    ime=input("Unesite ime:")
    prezime=input("Unesite prezime:")
    return pickle.dumps(FizickoLice(jmbg,ime,prezime))
def unos_jmbg():
    jmbg=input("Unesite jmbg:")
    return jmbg
def ispisi_lica(lica):
    sorted_lica = dict(sorted(lica.items(), key=lambda item: item[1].prezime))

    for lice in sorted_lica.values():
        print(lice.__str__())

klijentM=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
klijentM.connect(("localhost",7001))
print("Klijent uspesno povezan sa monitor serverom...")
portovi=klijentM.recv(1024).decode().split(',')
primarni_port=(int)(portovi[0])
sekundarni_port=(int)(portovi[1])
print(f"primarni port:{primarni_port}")
print(f"sekundarni port:{sekundarni_port}")

klijentM.close()
klijent1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
klijent1.connect(('localhost',primarni_port))
print("Klijent je uspesno povezan sa serverom1...")



while True:
    username=input("Unesite username:")
    password=input("Unesite password:")

    klijent1.send(pickle.dumps(Korisnik(username,[],password)))
    korisnik = pickle.loads(klijent1.recv(1024))
    print(korisnik.auth)
    if korisnik.auth==True:break
    print("Pogresno korisnicko ime ili lozinka...")

klijent2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
klijent2.connect(('localhost',sekundarni_port))
print("Klijent je uspesno povezan sa serverom2...")

while True:
    username=input("Unesite username:")
    password=input("Unesite password:")

    klijent2.send(pickle.dumps(Korisnik(username,[],password)))
    korisnik = pickle.loads(klijent2.recv(1024))
    print(korisnik.auth)
    if korisnik.auth==True:break
    print("Pogresno korisnicko ime ili lozinka...")


print("Uspesno ulogovani korisnici...")
while True:
    print("1.Dodaj lice\n2.Izmeni lice\n3.Procitaj lice po jmbg-u\n4.Obrisi lice\n5.Replikacija\n6.Ispisi sva lica\n7.Izlaz")
    opcija=input("Unesite opciju:")
    if opcija=="1":
        klijent1.send(("ADD").encode())
        klijent1.send(lice_za_slanje())
        odgovor=klijent1.recv(1024).decode()
        print(odgovor)
    if opcija == "2":
        klijent1.send(("CHANGE").encode())
        klijent1.send(lice_za_slanje())
        odgovor=klijent1.recv(1024).decode()
        print(odgovor)
    if opcija =="3":
        klijent1.send(("READ").encode())
        klijent1.send(unos_jmbg().encode())
        lice =klijent1.recv(1024).decode()
        print(lice)
    if opcija == "4":
        klijent1.send(("DELETE").encode())
        klijent1.send(unos_jmbg().encode())
        odgovor=klijent1.recv(1024).decode()
        print(odgovor)
    if opcija == "5":
        klijent1.send(("READALL").encode())
        lica = pickle.loads(klijent1.recv(1024)) 
        odgovor = klijent1.recv(1024).decode()
        klijent2.send(("WRITE_ALL").encode())
        klijent2.send(pickle.dumps(lica))
        odgovor=klijent2.recv(1024).decode()
        print(odgovor)
    if opcija == "6":
        klijent1.send(("READALL").encode())
        lica = pickle.loads(klijent1.recv(1024))
        ispisi_lica(lica) 
        odgovor = klijent1.recv(1024).decode()
        


    if opcija=="7":break

print("Konekcija se zatvara...")
klijent1.close()
        

    

