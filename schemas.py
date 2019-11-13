from typing import List, Dict

from pydantic import BaseModel

# class Signature(BaseModel):
#     r: str
#     s: str
#     v: int

class JadeResp(BaseModel):
    code: int = 0
    status: int = 0
    message: str = "OK"
    crypto: str = "ecc"
    timestamp: int= 0
    sig: Dict = {}
    result: Dict

class JadeReq(BaseModel):
    appid: str
    timestamp: int
    sig: str
    encode: str = "base64"
    hash: str = "sha3"
    lang: str = "cn"
    data: Dict

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
    coinType: str = None
    # from
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
    data: Dict = {}
    hash: str
    block: int = -1
    extraData: str = ""
    memo: str = ""
    sendAgain: bool = False

    class Config:
        orm_mode = True

# class Order_Signed(JadeResp):
#     result: Order_Result
