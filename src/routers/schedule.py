from fastapi import APIRouter, HTTPException
from src.models.schemas import LogisticsRequest
from src.services.schedule import optimize_schedule

router = APIRouter()

@router.post("/schedule")
async def schedule_tasks(request: LogisticsRequest):
    if not request.tasks:
        raise HTTPException(status_code=400, detail="No tasks provided")
    
    task_ids = {t.id for t in request.tasks}
    for t in request.tasks:
        for dep_id in t.dependencies:
            if dep_id not in task_ids:
                raise HTTPException(status_code=400, detail=f"Dependency {dep_id} not found in tasks")
    
    result = optimize_schedule(request)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return {"result": result}
