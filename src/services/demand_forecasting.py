from langchain.llms import OpenAI
from langchain.chains import TransformChain
import os
from dotenv import load_dotenv
load_dotenv()

llm = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY")
    )

def forecast_demand(inputs):
    return {"demand_forecast": llm.predict(f"Predict demand for: {inputs['market_data']}")}

forecast_chain = TransformChain(
    input_variables=["market_data"],
    output_variables=["demand_forecast"],
    transform=forecast_demand
)
from langchain.agents import Tool

constraint_analyzer = Tool(
    name="Constraint Analyzer",
    func=lambda constraints: llm.predict(f"Identify potential issues in: {constraints}"),
    description="Analyzes production constraints"
)
from fastapi import HTTPException

class SchedulingError(Exception):
    pass

async def validate_capacity(constraints):
    if constraints['demand'] > constraints['capacity']:
        raise HTTPException(
            status_code=400,
            detail="Insufficient production capacity"
        )