from pydantic import BaseModel
from datetime import datetime

class DemandForecast(BaseModel):
    product_id: str
    quantity: int
    due_date: datetime

class ResourceAvailability(BaseModel):
    machine_id: str
    available_hours: float
    maintenance_schedule: list[datetime]

class ProductionCapacity(BaseModel):
    max_shifts: int
    hours_per_shift: float
    downtime_factor: float

class ProductionPlanRequest(BaseModel):
    demand: list[DemandForecast]
    resources: list[ResourceAvailability]
    capacity: ProductionCapacity