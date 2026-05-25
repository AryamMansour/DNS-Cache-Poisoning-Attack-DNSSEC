from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
import base64

def sign(data, private_key):
    hash = SHA256.new(data.encode())
    signature = pkcs1_15.new(private_key).sign(hash)
    return base64.b64encode(signature).decode()

def verify(data, signature_b64, public_key):
    hash = SHA256.new(data.encode())

    try:
        signature = base64.b64decode(signature_b64)
        pkcs1_15.new(public_key).verify(hash, signature)
        return True
    except:
        return False
