from pydantic import BaseModel, Field, EmailStr
from typing import List, Dict, Optional

class Task(BaseModel):
    id: int
    name: str
    duration: int  
    dependencies: List[int] = []
    resources_required: Dict[str, int] = {}
    location: str
    priority: int = 0
    earliest_start: Optional[int] = None
    latest_end: Optional[int] = None
    cost_per_hour: Optional[float] = None  

class LogisticsRequest(BaseModel):
    tasks: List[Task]
    resource_pool: Dict[str, int]
    transit_matrix: Dict[str, Dict[str, int]]
    objective: str = 'makespan'
    vehicles: List[str]
