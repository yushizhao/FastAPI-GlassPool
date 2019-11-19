from typing import List, Dict
import time
import requests
import hashlib

from pydantic import BaseModel, Schema

from jadepool_signature import sign_jade_dict, flatten_jade_dict
from glassblock import GlassBlock
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

    def callback(self, url: str):
        return requests.post(url,json = self.dict()).json()

class JadeReq(BaseModel):
    appid: str
    timestamp: int
    sig: str
    encode: str = "base64"
    hash: str = "sha3"
    lang: str = "cn"
    data: Dict

class Address_Result(BaseModel):
    id: int = 0
    appid: str = "glasspool"
    type: str
    address: str
    state: str = "used"
    mode: str
    create_at: int
    update_at: int
    namespace: str = ""
    sid: str = ""

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
    blockHash: str
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
    sequence: int = -1
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

    @classmethod
    def init_order(cls, bizType: str, coinName: str, type: str, to: str, value: str, sequence: int = -1, memo: str = ""):
        ts = int(time.time()*1000)
        block = GlassBlock(type)

        return cls(
            coinName = coinName,
            state = "init",
            bizType = bizType,
            type = type,
            coinType = coinName,
            from_ = block.from_,
            to = to,
            value = value,
            sequence = sequence,
            confirmations = 0,
            create_at = ts,
            update_at = ts,
            hash = "",
            memo = memo
        )

    def get_updates(self, state: str):
        ts = int(time.time()*1000)
        block = GlassBlock(self.type)

        updates = {
            "update_at": ts,
            "state": state
        }

        if self.state == "init":
            m = hashlib.sha256()
            m.update(bytes(str(self.create_at).encode()))
            m.update(bytes(str(ts).encode()))
            txid = m.hexdigest()

            updates["txid"] = txid
            updates["from_"] = block.from_
            updates["hash"] = txid
            updates["block"] = block.get_number()
        
        if state == "pending":
            updates["confirmations"] = 1
        elif state == "done":
            updates["confirmations"] = block.confirmation

        return updates

    def to_result(self):
        if self.block == -1:
            blockHash = ""
        else:
            m = hashlib.sha256()
            m.update(bytes(str(self.block).encode()))
            m.update(self.type.encode())
            blockHash = m.hexdigest()
        
        self.data = Order_Result_Data(
            timestampBegin = self.create_at,
            type = self.type,
            hash = self.hash,
            blockNumber = self.block,
            blockHash = blockHash,
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

class Deposit(BaseModel):
    coinName: str
    value: str
    to: str
    memo: str = ""