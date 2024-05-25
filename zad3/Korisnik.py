class Korisnik:
    def __init__(self,username,privilages,password):
        self.username=username
        self.privilages = privilages
        self.password = password
        self.auth = False