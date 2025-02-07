from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import InventoryItem
from schemas import InventoryItemSchema

router = APIRouter()

@router.get("/inventory", response_model=list[InventoryItemSchema])
def get_inventory(db: Session = Depends(get_db)):
    return db.query(InventoryItem).all()

@router.post("/inventory")
def add_inventory_item(item: InventoryItemSchema, db: Session = Depends(get_db)):
    new_item = InventoryItem(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item
