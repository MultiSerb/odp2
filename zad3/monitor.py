import socket,time,pickle
from Korisnik import Korisnik

def azuriraj_stanje(server,stanje):
   
    server.send(stanje.encode())
    print(server.recv(1024).decode())




server1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server1.connect(('localhost',6000))
print("Monitor je uspesno povezan sa serverom1...")

time.sleep(1)

server2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server2.connect(('localhost',7000))
print("Monitor je uspesno povezan sa serverom2...")







azuriraj_stanje(server1,"primarni")
time.sleep(3)
azuriraj_stanje(server2,"sekundarni")

print("Zatvaranje konekcije sa klijentom...")
server1.close()
server2.close()

monitorS = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
monitorS.bind(('localhost',7001))
monitorS.listen()
print("Monitor server uspesno podesen...")
kanal,adresa = monitorS.accept()

kanal.send(("6000,7000").encode())
kanal.close()
 