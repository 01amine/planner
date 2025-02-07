from langchain.llms import OpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import json_loader
import os

llm = OpenAI(model_name="gpt-4", api_key=os.getenv("OPENAI_API_KEY"))

# Define the graph state
class InventoryState:
    def __init__(self, item_name, stock_level, reorder_threshold):
        self.item_name = item_name
        self.stock_level = stock_level
        self.reorder_threshold = reorder_threshold
        self.alert_needed = False

# Function: Check Stock Levels
def check_stock(state: InventoryState):
    if state.stock_level < state.reorder_threshold:
        state.alert_needed = True
    return state

# Function: Generate AI Alert Message
def generate_alert(state: InventoryState):
    if state.alert_needed:
        prompt = f"Stock level for {state.item_name} is low ({state.stock_level}). Generate a warning message."
        state.alert_message = llm(prompt)
    return state

# Build Graph
graph = StateGraph(InventoryState)
graph.add_node("check_stock", check_stock)
graph.add_node("generate_alert", generate_alert)

graph.add_edge("check_stock", "generate_alert")
graph.set_entry_point("check_stock")
graph.set_finish_point("generate_alert", END)

workflow = graph.compile()
