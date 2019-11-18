import time
from secrets import token_bytes

from eth_utils import keccak
from eth_utils.conversions import to_hex
from eth_keys import keys

def get_eth_address():
    pk = keys.PrivateKey(token_bytes(32))
    return pk.public_key.to_checksum_address()

class GlassBlock:
    def __init__(self, type: str):
        # to do: extend to other types
        if type == "ETH":
            self.chain = "ETH"
            self.blocktime = 12.5
            self.intercept = 116966214
            self.get_address = get_eth_address
        else:
            self.chain = "ETH"
            self.blocktime = 12.5
            self.intercept = 116966214
            self.get_address = get_eth_address
    
    def get_number_and_hash(self):
        n = int(time.time() / self.blocktime) - self.intercept
        hash_bytes = keccak(bytes(n) + self.chain.encode())
        return n, to_hex(hash_bytes)
        
