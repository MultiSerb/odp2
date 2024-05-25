class Lek:
    def __init__(self, id, naziv):
        self.id = id
        self.naziv = naziv

    def __str__(self) -> str:
        return f"{self.id} - {self.naziv}"

