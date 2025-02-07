from fastapi import FastAPI, WebSocket
from src.models.demande import ProductionPlanRequest
from src.routers import schedule, production
from src.services.production import ProductionScheduler

app = FastAPI()

app.include_router(schedule.router, tags=["Scheduling"])

@app.post("/generate-production-plan")
async def create_production_plan(request: ProductionPlanRequest):
    scheduler = ProductionScheduler(request)
    return await scheduler.generate_plan()

@app.websocket("/ws/production-updates")
async def websocket_production_updates(websocket: WebSocket):
    await websocket.accept()