import codecs

from eth_keys import keys

def get_public_key(private_key_base64: str):
    k = keys.PrivateKey(codecs.decode(private_key_base64.encode(),'base64'))
    public_key_bytes = k.public_key.to_bytes()
    return codecs.encode(public_key_bytes,'base64')