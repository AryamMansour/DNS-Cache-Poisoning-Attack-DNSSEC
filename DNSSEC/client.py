import socket
import random

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server = "192.168.56.102"
port = 5053

domain = input("Enter domain: ")
qid = str(random.randint(1000, 1100))

sock.sendto(f"{qid}|{domain}".encode(), (server, port))

data, _ = sock.recvfrom(1024)

try:
    _, ip = data.decode().split("|")
    print("IP:", ip)
except:
    print("Invalid response")
