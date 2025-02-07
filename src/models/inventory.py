from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base

class InventoryItem(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    stock_level = Column(Integer, default=0)
    reorder_threshold = Column(Integer, default=10)
    last_updated = Column(DateTime, default=func.now())
