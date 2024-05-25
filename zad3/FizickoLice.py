class FizickoLice:
    def __init__(self, jmbg,ime,prezime):
        self.jmbg = jmbg
        self.ime = ime
        self.prezime = prezime
    def __str__(self):
        return f"Lice:{self.ime} {self.prezime} JMBG:{self.jmbg}"
