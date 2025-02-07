from fastapi import FastAPI
from src.routers import schedule

app = FastAPI()

app.include_router(schedule.router, prefix="/api", tags=["Scheduling"])
