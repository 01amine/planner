from fastapi import FastAPI
from src.routers import schedule, production

app = FastAPI()

app.include_router(schedule.router, prefix="/api", tags=["Scheduling"])
app.include_router(production.router, prefix="/api", tags=["Production Planning"])