import socket
from Cryptodome.PublicKey import RSA
from crypto_functions import verify

PORT = 5053
ROOT_IP = "192.168.56.102"
ROOT_PORT = 5054

def get_key(file):
    return RSA.import_key(open(file, "rb").read())

root_ksk_public = get_key("ksk_public.pem")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", PORT))

cache = {}
pending = {}

print("Resolver running...")

while True:
    data, addr = sock.recvfrom(65535)
    parts = data.decode().split("|")

    # ================= ROOT RESPONSE =================
    if parts[0] == "ROOT":

        if len(parts) < 7:
            continue

        _, qid, record, record_sign, dnskey_sign, zsk_public_str, ksk_public_str = parts

        try:
            zsk_public = RSA.import_key(zsk_public_str.encode())
            ksk_public = RSA.import_key(ksk_public_str.encode())
        except:
            continue

        dnskey = zsk_public_str + "|" + ksk_public_str

        # DNSKEY verification
        if not verify(dnskey, dnskey_sign, root_ksk_public):
            print(f"[FAIL] DNSKEY verification failed for QID {qid}")
        else:
            print(f"[OK] DNSKEY verification succeeded for QID {qid}")

            # DATA verification
            if not verify(record, record_sign, zsk_public):
                print(f"[FAIL] DATA verification failed for QID {qid}")
            else:
                print(f"[OK] DATA verification succeeded for QID {qid}")

                domain, ip = record.split(":")

                if qid in pending:
                    cache[domain] = ip

                    print(f"[CACHE] Added: {domain} -> {ip}")
                    print("[CACHE CONTENT]")
                    for k in cache:
                        print(f"{k} -> {cache[k]}")

                    sock.sendto(f"{qid}|{ip}".encode(), pending[qid])
                    del pending[qid]

        continue

    # ================= CLIENT REQUEST =================
    if len(parts) == 2:
        qid, domain = parts

        if domain in cache:
            sock.sendto(f"{qid}|{cache[domain]}".encode(), addr)
        else:
            pending[qid] = addr
            sock.sendto(data, (ROOT_IP, ROOT_PORT))

        continue
