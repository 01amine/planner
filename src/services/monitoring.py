from database import SessionLocal
from models import InventoryItem
from stock_graph import workflow, InventoryState
from src.services.alerts import send_alert

def monitor_stock():
    db = SessionLocal()
    items = db.query(InventoryItem).all()

    for item in items:
        state = InventoryState(item.name, item.stock_level, item.reorder_threshold)
        result = workflow.invoke(state)

        if result.alert_needed:
            send_alert(result.alert_message)

    db.close()
