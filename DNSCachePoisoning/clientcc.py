import socket
import random

server_ip = "127.0.0.1"
port = 5053

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

domain = input("Enter domain: ")


qid = random.randint(1000, 1100)

message = f"{qid}|{domain}"
sock.sendto(message.encode(), (server_ip, port))

data, _ = sock.recvfrom(1024)
response = data.decode()

resp_qid, ip = response.split("|")

print("Received IP:", ip)
