from fastapi import APIRouter
from database import SessionLocal
from models import InventoryItem
from stock_graph import workflow, InventoryState
from src.services.alerts import send_alert

router = APIRouter()

@router.get("/monitor_stock")
def monitor_stock():
    db = SessionLocal()
    items = db.query(InventoryItem).all()
    for item in items:
        state = InventoryState(item.name, item.stock_level, item.reorder_threshold)
        result = workflow.invoke(state)
        if result.alert_needed:
            send_alert(item)
    return {"message": "Stock monitoring completed."}

