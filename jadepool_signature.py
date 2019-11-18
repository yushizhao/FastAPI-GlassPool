from typing import Dict, List
import codecs

from eth_utils import keccak
from coincurve import PrivateKey

def get_public_key(private_key_base64: str):
    k = PrivateKey(secret = codecs.decode(private_key_base64.encode(),'base64'))
    public_key_bytes = k.public_key.format(compressed=False)
    return codecs.encode(public_key_bytes,'base64')


def flatten_jade_dict(d: Dict):
    msg = ""
    for k, v in sorted(d.items()):
        msg = msg + k
        if isinstance(v, dict):
            msg = msg + flatten_jade_dict(v)
        elif isinstance(v, list):
            msg = msg + flatten_jade_list(v)
        else:
            msg = msg + str(v)
    return msg

def flatten_jade_list(l: List):
    msg = ""
    for i, e in enumerate(l):
        msg = msg + str(i)
        if isinstance(e, dict):
            msg = msg + flatten_jade_dict(e)
        elif isinstance(e, list):
            msg = msg + flatten_jade_list(e)
        else:
            msg = msg + str(e)
    return msg

def sign_jade_dict(private_key_base64: str, msg: str):
    k = PrivateKey(secret = codecs.decode(private_key_base64.encode(),'base64'))
    signature = k.sign_recoverable(message = msg.encode(), hasher = keccak)
    jade_sig = {
        "r": codecs.encode(signature[:32],'base64')[:-1].decode(),
        "s": codecs.encode(signature[32:64],'base64')[:-1].decode(),
        "v": int(signature[64]) + 27
    }
    return jade_sig
