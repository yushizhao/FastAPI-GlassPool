import time
from secrets import token_bytes, token_urlsafe

from eth_utils.conversions import to_hex
from eth_keys import keys

def get_eos_address():
    return f"glasspool-deposit[{token_urlsafe(6)}]"

def get_eth_address():
    pk = keys.PrivateKey(token_bytes(32))
    return pk.public_key.to_checksum_address()

class GlassBlock:
    def __init__(self, type: str):
        # to do: extend to other types
        if type == "EOS":
            self.chain = "EOS"
            self.blocktime = 2
            self.intercept = 696546381
            self.use_memo = True
            self.get_address = get_eos_address
        else:
            self.chain = "ETH"
            self.blocktime = 12.5
            self.intercept = 116966214
            self.use_memo = False
            self.get_address = get_eth_address
    
    def get_number(self):
        n = int(time.time() / self.blocktime) - self.intercept
        return n
