from langchain.agents import Tool
from langchain.llms import OpenAI
import os


llm = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY")
)


constraint_analyzer = Tool(
    name="Constraint Analyzer",
    func=lambda constraints: llm.predict(f"Identify potential issues in: {constraints}"),
    description="Analyzes production constraints",
)