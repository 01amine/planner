from ortools.sat.python import cp_model
from src.models.schemas import LogisticsRequest

def optimize_schedule(request: LogisticsRequest) -> dict:
    tasks = request.tasks
    resource_pool = request.resource_pool
    transit_matrix = request.transit_matrix
    objective = request.objective

    model = cp_model.CpModel()
    solver = cp_model.CpSolver()

    max_time = sum(task.duration for task in tasks) * 2

    start_times = {}
    end_times = {}
    for task in tasks:
        min_start = task.earliest_start if task.earliest_start is not None else 0
        max_end = task.latest_end if task.latest_end is not None else max_time
        max_start = max_end - task.duration if task.latest_end is not None else max_time - task.duration

        if min_start > max_start:
            return {"error": f"Task {task.id} has impossible time window"}

        start_var = model.NewIntVar(min_start, max_start, f'start_{task.id}')
        end_var = model.NewIntVar(min_start + task.duration, max_end, f'end_{task.id}')
        model.Add(end_var == start_var + task.duration)
        start_times[task.id] = start_var
        end_times[task.id] = end_var

    
    for task in tasks:
        for dep_id in task.dependencies:
            dep_task = next((t for t in tasks if t.id == dep_id), None)
            if not dep_task:
                return {"error": f"Dependency {dep_id} not found"}
            transit_time = transit_matrix.get(dep_task.location, {}).get(task.location, 0)
            model.Add(start_times[task.id] >= end_times[dep_id] + transit_time)

   
    for resource, capacity in resource_pool.items():
        intervals = []
        demands = []
        for task in tasks:
            req = task.resources_required.get(resource, 0)
            if req > 0:
                interval = model.NewIntervalVar(
                    start_times[task.id],
                    task.duration,
                    end_times[task.id],
                    f'{resource}_interval_{task.id}'
                )
                intervals.append(interval)
                demands.append(req)
        if intervals:
            model.AddCumulative(intervals, demands, capacity)

    
    obj_var = model.NewIntVar(0, max_time, 'makespan')
    model.AddMaxEquality(obj_var, [end_times[t.id] for t in tasks])
    if objective == 'makespan':
        sum_priority = sum(t.priority for t in tasks)
        K = max_time * sum_priority + 1 if sum_priority else 1
        model.Minimize(obj_var * K + sum(start_times[t.id] * t.priority for t in tasks))
    elif objective == 'cost':
        if not any(t.cost_per_hour is not None and t.cost_per_hour > 0 for t in tasks):
            return {"error": "Cost objective requires tasks with cost_per_hour"}
        scale = 100  # scale dollars to cents
        cost_terms = [
            (end_times[t.id] - start_times[t.id]) * int(t.cost_per_hour * scale)
            for t in tasks if t.cost_per_hour is not None and t.cost_per_hour > 0
        ]
        total_cost = sum(cost_terms)
        model.Minimize(total_cost)
    else:
        return {"error": "Invalid objective specified"}

    
    num_vehicles = len(request.vehicles)
    vehicle_assignment = {task.id: model.NewIntVar(0, num_vehicles - 1, f"vehicle_{task.id}") for task in tasks}
    vehicle_intervals = {v: [] for v in range(num_vehicles)}
    for task in tasks:
        for v in range(num_vehicles):
            assigned = model.NewBoolVar(f"task_{task.id}_assigned_to_vehicle_{v}")
            model.Add(vehicle_assignment[task.id] == v).OnlyEnforceIf(assigned)
            model.Add(vehicle_assignment[task.id] != v).OnlyEnforceIf(assigned.Not())
            veh_interval = model.NewOptionalIntervalVar(
                start_times[task.id],
                task.duration,
                end_times[task.id],
                assigned,
                f"task_{task.id}_vehicle_{v}_interval"
            )
            vehicle_intervals[v].append(veh_interval)
    for v in range(num_vehicles):
        if vehicle_intervals[v]:
            model.AddNoOverlap(vehicle_intervals[v])

    status = solver.Solve(model)
    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        schedule = {}
        for t in tasks:
            veh_idx = solver.Value(vehicle_assignment[t.id])
            schedule[t.name] = {
                "start": solver.Value(start_times[t.id]),
                "end": solver.Value(end_times[t.id]),
                "resources": t.resources_required,
                "location": t.location,
                "vehicle": request.vehicles[veh_idx]
            }
        result = {
            "schedule": schedule,
            "makespan": solver.Value(obj_var) if objective == 'makespan' else None,
            "total_cost": solver.ObjectiveValue() if objective == 'cost' else None
        }
        return result
    else:
        return {"error": "No solution found"}
