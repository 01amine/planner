from fastapi import HTTPException

class SchedulingError(Exception):
    """
    Custom exception for scheduling-related errors.
    """
    pass

async def validate_capacity(constraints):
    """
    Validates if production capacity meets demand.
    Raises an HTTPException if capacity is insufficient.
    """
    if constraints['demand'] > constraints['capacity']:
        raise HTTPException(
            status_code=400,
            detail="Insufficient production capacity",
        )