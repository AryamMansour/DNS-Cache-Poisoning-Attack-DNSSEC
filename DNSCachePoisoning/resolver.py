import socket

resolver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
resolver.bind(("0.0.0.0", 5053))

cache = {}
saved_qid = {}   

root_ip = "127.0.0.1"
root_port = 5054

print("Resolver running...")

while True:
    data, addr = resolver.recvfrom(1024)
    message = data.decode()

    if ":" in message and "|" in message:
        qid_part, rest = message.split("|")
        domain, received_ip = rest.split(":")
        qid = int(qid_part)

        if qid in saved_qid and domain not in cache:
            cache[domain] = received_ip
            client_addr = saved_qid[qid]

            print(f"[Response] {domain} -> {received_ip}")

            reply = f"{qid}|{received_ip}"
            resolver.sendto(reply.encode(), client_addr)

            del saved_qid[qid]

        continue

    if "|" in message:
        qid_part, domain = message.split("|")
        qid = int(qid_part)

        if domain in cache:
            ip = cache[domain]
            reply = f"{qid}|{ip}"
            resolver.sendto(reply.encode(), addr)

        else:
            
            saved_qid[qid] = addr

            forward = f"{qid}|{domain}"
            resolver.sendto(forward.encode(), (root_ip, root_port))

    elif "|" in message:
        qid_part, ip = message.split("|")
        qid = int(qid_part)

        if qid in saved_qid:
            client_addr = saved_qid[qid]

            reply = f"{qid}|{ip}"
            resolver.sendto(reply.encode(), client_addr)

            del saved_qid[qid]
