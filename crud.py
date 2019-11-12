from sqlalchemy.orm import Session

import models
import schemas

def create_order(db: Session, order: schemas.Order_Result):
    db_order = models.Order_ORM(
        txid = order.txid,
        sequence = order.sequence,
        coinName = order.coinName,
        state = order.state,
        bizType = order.bizType,
        type = order.type,
        to = order.to,
        value = order.value,
        create_at = order.create_at,
        update_at = order.update_at
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order(db: Session, id: int):
    return db.query(models.Order_ORM).filter(models.Order_ORM.id == id).first()