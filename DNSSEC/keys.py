from Cryptodome.PublicKey import RSA

def save_key(name, key):
    open(f"{name}_private.pem", "wb").write(key.export_key())
    open(f"{name}_public.pem", "wb").write(key.publickey().export_key())

save_key("ksk", RSA.generate(2048))
save_key("zsk", RSA.generate(2048))

print("Keys generated and saved.")
