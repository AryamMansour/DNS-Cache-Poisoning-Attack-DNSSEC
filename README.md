# DNS-Cache-Poisoning-Attack-DNSSEC
Simulation of a DNS cache poisoning attack and DNSSEC as a countermeasure. Includes a full attack environment (client, resolver, root server, and attacker) with DNSSEC implementation that successfully rejects forged responses using cryptographic signatures.

All codes are written in python and tested on Kali Linux and Ubuntu VMs by Aryam Mansour, Rand I. H. Abualqumssan, Razan Hamchou and Rawdha Abdelaziz as a part of Computer and network security course in University of Sharjah.


To run DNS Cache Poisoning Attack:

1 - Configure 2 VMs and allow communication between them.

2 - Run resolver.py and root.py on machine 1.

3 - Run attacker.py on machine 2.

4 - Run clientcc.py on machine 1 right after running the attack.

To run DNSSEC:

1 - Configure 2 VMs and allow communication between them.

2 - Generate keys bu running keys.py on machine 1.

3 - Run root.py and resolver.py on machine 1.

4 - Run attacker.py on machine 2.

5 - Run client.py on machine 1 right after running the attack.
