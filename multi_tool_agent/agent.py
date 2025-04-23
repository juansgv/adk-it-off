import os
from google.adk.agents import Agent

from google.adk.agents import LlmAgent
from google.adk.tools import google_search

from youtube_shorts_assistant.util import load_instruction_from_file

# Subagents

# 1. ScriptWriter
script_writer_agent = LlmAgent(
    name="script_writer_agent",
    model="gemini-2.5-pro-exp-03-25",
    instruction=load_instruction_from_file("script_writer_agent_instruction.txt"),
    tools=[google_search],
    output_key="generated_script", # Save result to state
)

# 2. Visualizer
visual_editor_agent = LlmAgent(
    name="visual_editor_agent",
    model="gemini-2.0-flash",
    instruction=load_instruction_from_file("visual_editor_agent_instruction.txt"),
    description="Generates visual concepts based on a provided script.",
    output_key="generated_visuals", # Save result to state
)

# 3. Formatters
formatter_agent = LlmAgent(
    name="ConceptFormatter",
    model="gemini-2.0-flash",
    instruction="""Combine the script from state ['generated_script'] and the visual concepts from state ['generated_visuals'] into a final Markdown.""",
    description="Formats the final short concept.",
    output_key="final_short_concept"
)

# LLM Agent
youtube_shorts_agent = LlmAgent(
    name="youtube_shorts_agent",
    model="gemini-2.5-pro-exp-03-25",
    description="You are a ShortForm Genius, an AI specialized in crafting engaging Youtube Shorts content. Your expertise lies in generating content.",
    instruction=load_instruction_from_file("shorts_agent_instruction.txt"),
    sub_agents=[script_writer_agent,
                visual_editor_agent,
                formatter_agent
                ]
)

# Run the Root agent
root_agent = youtube_shorts_agent


def list_products(shop_id: str) -> dict:
    """Lists products for a given ecommerce shop."""
    return {"status": "success", "products": []}

def update_stock(product_id: str, quantity: int) -> dict:
    """Updates stock level for a product."""
    return {"status": "success", "product_id": product_id, "new_quantity": quantity}

def process_order(order_id: str) -> dict:
    """Processes an order by ID."""
    return {"status": "success", "order_id": order_id}

def get_sales_report(period: str) -> dict:
    """Generates sales report for a period."""
    return {"status": "success", "period": period, "report": {}}

def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    from datetime import datetime
    from zoneinfo import ZoneInfo
    key = city.lower()
    if key in ("new york",):
        tz = ZoneInfo("America/New_York")
    elif key in ("bogota", "colombia"):
        tz = ZoneInfo("America/Bogota")
    else:
        return {"status": "error", "error_message": f"Timezone for {city} not available."}
    now = datetime.now(tz)
    return {"status": "success", "report": now.strftime("%Y-%m-%d %H:%M:%S %Z")}

root_agent = Agent(
    name="it_office_agent",
    model=os.getenv("ADK_MODEL", "gemini-2.0-flash"),
    description="Manage products, stock, orders & reports for ecommerce shops.",
    instruction="You are a helpful IT‑Office agent for ecommerce operations.",
    tools=[list_products, update_stock, process_order, get_sales_report, get_current_time],
)
