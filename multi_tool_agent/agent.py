import os
from google.adk.agents import Agent

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
