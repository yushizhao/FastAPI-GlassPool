import time
import hashlib

import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from glasspool_logging import glassflow_log
from glasspool_config import config
from jadepool_signature import get_public_key
from glassblock import GlassBlock
import schemas
from database import get_db
import models
import crud

app = FastAPI()

@app.get("/")
async def root():
    glassflow_log.debug(config["privateKey"])
    return {"message": "Hello World"}

@app.get("/publicKey")
async def get_publicKey():
    return {"message": get_public_key(config["privateKey"])}

@app.post("/api/v2/address/{coinName}/new",response_model = schemas.JadeResp)
async def post_api_v2_address__new(coinName: str, req: schemas.JadeReq):
    ts = int(time.time()*1000)
    asset = config.get("assets").get(coinName, {})
    address = GlassBlock(asset.get("type","")).get_address()
    
    address_res = schemas.Address_Result(
        type = coinName,
        address = address,
        mode = req.data.get("mode"),
        create_at = ts,
        update_at = ts
    )

    address_resp =  schemas.JadeResp(result = address_res.dict())
    address_resp.sign(config["privateKey"])
    return address_resp

@app.get("/api/v2/orders/{id}", response_model = schemas.JadeResp)
def get_api_v2_orders_(id: int, db: Session = Depends(get_db)):
    order_orm = crud.get_order(db = db, id = id)
    order_res = schemas.Order_Result.from_orm(order_orm).to_result()
    order_resp = schemas.JadeResp(result = order_res.dict(by_alias=True))
    order_resp.sign(config["privateKey"])
    return order_resp

@app.post("/api/v2/wallet/{coinName}/withdraw", response_model = schemas.JadeResp)
def post_api_v2_wallet__withdraw(coinName: str, req: schemas.JadeReq, db: Session = Depends(get_db)):
    asset = config.get("assets").get(coinName, {})

    order_init = schemas.Order_Result.init_order(
        bizType = "WITHDRAW",
        coinName = coinName,
        type = asset.get("type",""),
        to = req.data.get("to",""),
        value = req.data.get("value",""),
        sequence = req.data.get("sequence")
    )

    order_orm = crud.create_order(db = db, order = order_init)
    order_res = schemas.Order_Result.from_orm(order_orm).to_result()
    order_resp = schemas.JadeResp(result = order_res.dict(by_alias=True))
    order_resp.sign(config["privateKey"])
    return order_resp

@app.post("/deposit")
def post_deposit(deposit: schemas.Deposit, db: Session = Depends(get_db)):
    asset = config.get("assets").get(deposit.coinName, {})

    order_init = schemas.Order_Result.init_order(
        bizType = "DEPOSIT",
        coinName = deposit.coinName,
        type = asset.get("type"),
        to = deposit.to,
        value = deposit.value,
        memo = deposit.memo
    )

    order_orm = crud.create_order(db = db, order = order_init)
    return {"id": order_orm.id}

@app.post("/callback/raw")
async def post_callback_raw(order_res: schemas.Order_Result):
    order_resp = schemas.JadeResp(result = order_res.to_result().dict(by_alias=True))
    order_resp.sign(config["privateKey"])
    return order_resp.callback(config["callback"])

@app.post("/callback/cooked")
def get_callback_cooked(state: str, id: int, db: Session = Depends(get_db)):
    order_orm = crud.get_order(db = db, id = id)
    updates = schemas.Order_Result.from_orm(order_orm).get_updates(state)
    crud.update_order(db = db, id = id, updates = updates)

    order_orm = crud.get_order(db = db, id = id)
    order_res = schemas.Order_Result.from_orm(order_orm).to_result()
    order_resp = schemas.JadeResp(result = order_res.dict(by_alias=True))
    order_resp.sign(config["privateKey"])
    return order_resp.callback(config["callback"])

@app.get("/orders/{state}")
def get_orders______(state: str, page: int = 0, page_size: int = 100, db: Session = Depends(get_db)):
    order_orms = crud.get_order_by_state(db = db, state = state, page = page, page_size = page_size)
    return [schemas.Order_Result.from_orm(o).dict(by_alias=True) for o in order_orms]

if __name__ == "__main__":
    models.create_tables()
    uvicorn.run(app, host = config["host"], port = config["port"])