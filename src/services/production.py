import os
from typing import Dict, List
from datetime import datetime
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
import pulp  
from src.models.demande import ProductionPlanRequest


class ProductionScheduler:
    def __init__(self, request: ProductionPlanRequest):
        self.request = request
        self.constraints = self._parse_constraints()

    async def generate_plan(self) -> Dict:
        """
        Generates an optimized production schedule and provides a natural language explanation.
        """
        
        optimized_plan = await self._optimize_schedule()

        
        return {
            "schedule": optimized_plan,
            "explanation": self._generate_narrative(optimized_plan),
        }

    def _parse_constraints(self) -> Dict:
        """
        Parses the request into mathematical constraints for optimization.
        """
        return {
            "demand": {d.product_id: d.quantity for d in self.request.demand},
            "capacity": self._calculate_effective_capacity(),
        }

    def _calculate_effective_capacity(self) -> float:
        """
        Calculates the effective production capacity based on shifts, hours, and downtime.
        """
        capacity = self.request.capacity
        effective_capacity = (
            capacity.max_shifts * capacity.hours_per_shift * (1 - capacity.downtime_factor)
        )
        return effective_capacity

    async def _optimize_schedule(self) -> Dict[str, List[Dict]]:
        """
        Optimizes the production schedule using linear programming (PuLP).
        """
        
        problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

        
        products = [d.product_id for d in self.request.demand]
        machines = [r.machine_id for r in self.request.resources]

       
        production_vars = pulp.LpVariable.dicts(
            "Production", [(m, p) for m in machines for p in products], lowBound=0, cat="Integer"
        )

        
        problem += pulp.lpSum(
            production_vars[m, p] for m in machines for p in products
        ), "Total_Production"

        
        for p in products:
            problem += (
                pulp.lpSum(production_vars[m, p] for m in machines) >= self.constraints["demand"][p],
                f"Demand_{p}",
            )

        for m in machines:
            problem += (
                pulp.lpSum(production_vars[m, p] for p in products) <= self.constraints["capacity"],
                f"Capacity_{m}",
            )

        
        problem.solve()

        
        optimized_schedule = {}
        for m in machines:
            optimized_schedule[m] = []
            for p in products:
                if production_vars[m, p].varValue > 0:
                    optimized_schedule[m].append(
                        {"product": p, "quantity": production_vars[m, p].varValue}
                    )

        return optimized_schedule

    def _generate_narrative(self, schedule: Dict[str, List[Dict]]) -> str:
        """
        Generates a natural language explanation of the production schedule using LangChain.
        """
        
        prompt = PromptTemplate(
            template="Explain this production schedule: {schedule}",
            input_variables=["schedule"],
        )

        
        llm = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
        )

        
        chain = LLMChain(llm=llm, prompt=prompt)
        explanation = chain.run(schedule=schedule)

        return explanation