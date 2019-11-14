import codecs

# from eth_keys import keys
from coincurve import PrivateKey

def get_public_key(private_key_base64: str):
    k = PrivateKey(secret = codecs.decode(private_key_base64.encode(),'base64'))
    public_key_bytes = k.public_key.format(compressed=False)
    return codecs.encode(public_key_bytes,'base64')