from fastapi import APIRouter
from src.models.schemas import LogisticsRequest
from src.models.demande import ProductionPlanRequest
from src.services.schedule import optimize_schedule

router = APIRouter()



@router.post("/optimize_logistics")
def optimize_logistics(request: LogisticsRequest):
    result = optimize_schedule(request)
    return result

