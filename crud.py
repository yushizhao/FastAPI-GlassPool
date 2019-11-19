from typing import Dict
from sqlalchemy.orm import Session

import models
import schemas

def create_order(db: Session, order: schemas.Order_Result):
    db_order = models.Order_ORM(
        txid = order.txid,
        coinName = order.coinName,
        state = order.state,
        bizType = order.bizType,
        type = order.type,
        coinType = order.coinType,
        from_ = order.from_,
        to = order.to,
        value = order.value,
        sequence = order.sequence,
        confirmations = order.confirmations,
        create_at = order.create_at,
        update_at = order.update_at,
        hash = order.hash,
        block = order.block,
        memo = order.memo
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order(db: Session, id: int):
    return db.query(models.Order_ORM).filter(models.Order_ORM.id == id).first()

def update_order(db: Session, id: int, updates: Dict):
    db.query(models.Order_ORM).filter(models.Order_ORM.id == id).update(updates, synchronize_session=False)
    db.commit()
