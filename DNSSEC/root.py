import socket
import time
from Cryptodome.PublicKey import RSA
from crypto_functions import sign

ROOT_IP = "192.168.56.102"
PORT = 5054

def get_key(file):
    return RSA.import_key(open(file, "rb").read())

ksk_private = get_key("ksk_private.pem")
ksk_public  = get_key("ksk_public.pem")
zsk_private = get_key("zsk_private.pem")
zsk_public  = get_key("zsk_public.pem")

records = {
    "example.com": "93.184.216.34",
    "google.com": "142.250.190.14"
}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", PORT))

print("ROOT running...")
time.sleep(5)

while True:
    data, addr = sock.recvfrom(65535)
    qid, domain = data.decode().split("|")

    ip = records.get(domain, "1.1.1.1")
    record = f"{domain}:{ip}"

    record_sign = sign(record, zsk_private)

    dnskey = zsk_public.export_key().decode() + "|" + ksk_public.export_key().decode()
    dnskey_sign = sign(dnskey, ksk_private)

    message = "|".join([
        "ROOT",
        qid,
        record,
        record_sign,
        dnskey_sign,
        zsk_public.export_key().decode(),
        ksk_public.export_key().decode()
    ])

    sock.sendto(message.encode(), addr)

    print(f"[ROOT] Sent to {addr}")
    print(f"[ROOT] QID: {qid} | Record: {record}")
