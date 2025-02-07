from fastapi import APIRouter
from src.models.schemas import LogisticsRequest
from src.models.demande import ProductionPlanRequest
from src.services.production import ProductionScheduler

router = APIRouter()
@router.post("/generate_production_plan")
async def generate_production_plan(request: ProductionPlanRequest):
    scheduler = ProductionScheduler(request)
    result = await scheduler.generate_plan()
    return result
