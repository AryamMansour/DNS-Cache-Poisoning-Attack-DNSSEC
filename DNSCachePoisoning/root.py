import socket
import time

time.sleep(5)

root = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
root.bind(("0.0.0.0", 5054))

records = {
    "example.com": "93.184.216.34",
    "google.com": "142.250.190.14"
}

print("Root server running...")

while True:
    data, addr = root.recvfrom(1024)
    message = data.decode()

    if "|" in message:
        qid_part, domain = message.split("|")
        qid = int(qid_part)

        if domain in records:
            ip = records[domain]
        else:
            ip = "1.1.1.1"
        time.sleep(2)
        reply = f"{qid}|{domain}:{ip}"
        root.sendto(reply.encode(), addr)
