import socket

def azuriraj_stanje(socket, stanje):
    socket.send(stanje.encode())
    print(socket.recv(1024).decode())

def main():
    monitorP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    monitorS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        monitorP.connect(('localhost', 6000))
        print("Veza sa primarnim serverom je uspostavljena.")

        azuriraj_stanje(monitorP, "primarni")
    except Exception as ex:
        print(ex)

    try:
        monitorS.connect(('localhost', 7000))
        print("Veza sa sekundarnim serverom je uspostavljena.")

        azuriraj_stanje(monitorS, "sekundarni")
    except Exception as ex:
        print(ex)

    print("Zatvaranje konekcija.")
    monitorP.close()
    monitorS.close()

    monitor_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    monitor_server.bind(('localhost', 3000))
    monitor_server.listen()
    print("Server monitora je pokrenut.")

    kanal, adresa = monitor_server.accept()
    print(f"Prihvacena je konekcija klijenta sa adrese: {adresa}")

    kanal.send(("6000,7000").encode())
    print("Poslati portovi, zatvaranje konekcije.")
    kanal.close()
    
main()