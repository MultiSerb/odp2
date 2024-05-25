from korisnik import Korisnik
import hashlib

korisnici = {}

def hesiranje(tekst):
    return hashlib.sha256(tekst.encode()).hexdigest()

def dodaj_korisnika(korisnicko_ime, lozinka):
    korisnici[korisnicko_ime] = Korisnik(korisnicko_ime, hesiranje(lozinka))

def autentifikacija(korisnicko_ime, lozinka):
    if (korisnicko_ime in korisnici) and (hesiranje(lozinka) == korisnici[korisnicko_ime].lozinka):
        korisnici[korisnicko_ime].autentifikovan = True
        return True
    else:
        return False