from typing import List, Dict
import time

from pydantic import BaseModel, Schema

from jadepool_signature import sign_jade_dict, flatten_jade_dict

# from glasspool_logging import glassflow_log

# class JadeSig(BaseModel):
#     r: str
#     s: str
#     v: int

class JadeResp(BaseModel):
    code: int = 0
    status: int = 0
    message: str = "OK"
    crypto: str = "ecc"
    timestamp: int = 0
    sig: Dict = {}
    result: Dict = {}

    def sign(self, private_key_base64: str):
        self.timestamp = int(time.time()*1000)
        msg = f"{flatten_jade_dict(self.result)}timestamp{self.timestamp}"
        # glassflow_log.debug(msg)
        self.sig = sign_jade_dict(private_key_base64 = private_key_base64, msg = msg)
        
class JadeReq(BaseModel):
    appid: str
    timestamp: int
    sig: str
    encode: str = "base64"
    hash: str = "sha3"
    lang: str = "cn"
    data: Dict

class Order_Result_Data_FromTo(BaseModel):
    address: str
    value: str
    asset: str

class Order_Result_Data(BaseModel):
    timestampBegin: int
    timestampFinish: int = 0
    nonce: int = 0
    type: str
    hash: str
    blockNumber: int
    blockHash: str = "0x"
    from_: List[Order_Result_Data_FromTo]
    to: List[Order_Result_Data_FromTo]
    fee: str
    confirmations: int

    class Config:
        allow_population_by_alias = True
        fields = {'from_': {'alias': 'from'}}

class Order_Result(BaseModel):
    _id: str = ""
    id: str = "to be assigned by database"
    coinName: str
    txid: str = None
    meta: str = None
    state: str
    bizType: str 
    type: str
    subType: str = ""
    coinType: str
    from_: str
    to: str
    value: str
    sequence: int
    confirmations: int = 0
    create_at: int
    update_at: int
    actionArgs: List = []
    actionResults: List = []
    n: int = 0
    fee: str = "0"
    fees: List = []
    data: Order_Result_Data = None
    hash: str
    block: int = -1
    extraData: str = ""
    memo: str = ""
    sendAgain: bool = False

    class Config:
        allow_population_by_alias = True
        orm_mode = True
        fields = {'from_': {'alias': 'from'}}

    def to_result(self):
        self.data = Order_Result_Data(
            timestampBegin = self.create_at,
            type = self.type,
            hash = self.hash,
            blockNumber = self.block,
            from_ = [
                Order_Result_Data_FromTo(
                address = self.from_,
                value = self.value,
                asset = self.coinType
            )
            ],
            to = [
                Order_Result_Data_FromTo(
                address = self.to,
                value = self.value,
                asset = self.coinType
            )
            ],
            fee = self.fee,
            confirmations = self.confirmations
        )
        return self

        

# class Order_Signed(JadeResp):
#     result: Order_Result
