# Google Agent Development Kit (ADK) Implementation Documentation

## Table of Contents
- [Overview](#overview)
- [Installation & Setup](#installation--setup)
- [Project Architecture](#project-architecture)
- [Agent Implementations](#agent-implementations)
  - [YouTube Shorts Content Generation Agent](#youtube-shorts-content-generation-agent)
  - [IT Office Ecommerce Agent](#it-office-ecommerce-agent)
- [Usage Examples](#usage-examples)
- [Extending the Agents](#extending-the-agents)

## Overview

This project showcases two implementations of Google's Agent Development Kit (ADK):

1. **YouTube Shorts Content Generation System**: A multi-agent system that generates script and visual concepts for YouTube Shorts content
2. **IT Office Ecommerce Agent**: A practical agent for managing ecommerce operations including product inventory, orders, and reporting

Both implementations demonstrate the power of Google's ADK for building specialized AI agents powered by Gemini models.

## Installation & Setup

### Prerequisites
- Python 3.9 or higher
- Google API credentials with access to Gemini models

### Installation Steps

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd adk_it_office
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements/base.txt
   # For development: pip install -r requirements/dev.txt
   ```

4. Configure environment variables:
   ```
   # Create a .env file in the multi_tool_agent directory
   ADK_MODEL="gemini-2.0-flash"  # Or your preferred Gemini model
   # Add your Google API keys and other configuration
   ```

## Project Architecture

The project is structured as follows:

```
adk_it_office/
├── multi_tool_agent/
│   ├── __init__.py
│   ├── .env               # Environment configuration
│   └── agent.py           # Main agent implementations
└── requirements/
    ├── base.txt           # Base dependencies
    ├── dev.txt            # Development dependencies
    └── prod.txt           # Production dependencies
```

Key components:
- `agent.py`: Contains the core implementations of both agent systems
- `requirements/`: Contains dependency specifications for different environments

## Agent Implementations

### YouTube Shorts Content Generation Agent

The YouTube Shorts agent is a hierarchical multi-agent system designed to generate engaging short-form video content concepts.

#### Architecture

The system consists of a root agent and three specialized sub-agents:

1. **ScriptWriter Agent**
   - Generates script content for YouTube Shorts
   - Uses Gemini 2.5 Pro model
   - Integrates with Google Search for up-to-date information
   - Stores output in state using `output_key="generated_script"`

2. **Visual Editor Agent**
   - Generates visual concepts based on the provided script
   - Uses Gemini 2.0 Flash model
   - Stores output in state using `output_key="generated_visuals"`

3. **Formatter Agent**
   - Combines the script and visual concepts into a final markdown document
   - Uses Gemini 2.0 Flash model
   - Produces the final output as `final_short_concept`

#### Implementation Details

```python
# 1. ScriptWriter
script_writer_agent = LlmAgent(
    name="script_writer_agent",
    model="gemini-2.5-pro-exp-03-25",
    instruction=load_instruction_from_file("script_writer_agent_instruction.txt"),
    tools=[google_search],
    output_key="generated_script",  # Save result to state
)

# 2. Visualizer
visual_editor_agent = LlmAgent(
    name="visual_editor_agent",
    model="gemini-2.0-flash",
    instruction=load_instruction_from_file("visual_editor_agent_instruction.txt"),
    description="Generates visual concepts based on a provided script.",
    output_key="generated_visuals",  # Save result to state
)

# 3. Formatters
formatter_agent = LlmAgent(
    name="ConceptFormatter",
    model="gemini-2.0-flash",
    instruction="""Combine the script from state ['generated_script'] and the visual concepts from state ['generated_visuals'] into a final Markdown.""",
    description="Formats the final short concept.",
    output_key="final_short_concept"
)

# Root Agent
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
```

### IT Office Ecommerce Agent

The IT Office agent is designed to manage ecommerce operations through specialized tools.

#### Features

The IT Office agent provides the following functionality:
- Product listing and inventory management
- Order processing
- Sales reporting
- Time zone information retrieval

#### Implementation Details

```python
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

# Root Agent Definition
root_agent = Agent(
    name="it_office_agent",
    model=os.getenv("ADK_MODEL", "gemini-2.0-flash"),
    description="Manage products, stock, orders & reports for ecommerce shops.",
    instruction="You are a helpful IT‑Office agent for ecommerce operations.",
    tools=[list_products, update_stock, process_order, get_sales_report, get_current_time],
)
```

## Usage Examples

### Running the YouTube Shorts Agent

```python
from google.adk.runners import InMemoryRunner
from multi_tool_agent.agent import youtube_shorts_agent

# Create a runner
runner = InMemoryRunner(agent=youtube_shorts_agent, app_name="YouTubeShortsApp")

# Generate a YouTube Short concept
for event in runner.run(
    user_id="user123",
    session_id="session456",
    new_message="Create a YouTube Short about artificial intelligence for beginners"
):
    # Process events as they come in
    print(f"Event from {event.author}: {event.text}")
    
    # The final output will be in the session state
    if event.is_final_response():
        final_concept = runner.get_session(
            app_name="YouTubeShortsApp",
            user_id="user123",
            session_id="session456"
        ).state.get("final_short_concept")
        
        print("Final YouTube Short Concept:")
        print(final_concept)
```

### Running the IT Office Agent

```python
from google.adk.runners import InMemoryRunner
from multi_tool_agent.agent import root_agent as it_office_agent

# Create a runner
runner = InMemoryRunner(agent=it_office_agent, app_name="EcommerceApp")

# Example: Update product stock
for event in runner.run(
    user_id="admin",
    session_id="inventory_session",
    new_message="Update stock for product ABC123 to 50 units"
):
    print(f"Event from {event.author}: {event.text}")
    
    # Process function calls and responses
    for function_call in event.get_function_calls():
        print(f"Function called: {function_call.name}")
        print(f"Arguments: {function_call.args}")
        
    for function_response in event.get_function_responses():
        print(f"Function response: {function_response.response}")
```

## Extending the Agents

### Adding New Tools to the IT Office Agent

To add a new tool to the IT Office agent:

1. Define a new function with appropriate type hints:
   ```python
   def process_return(return_id: str, reason: str) -> dict:
       """Processes a customer return with the given ID and reason."""
       # Implement return processing logic
       return {"status": "success", "return_id": return_id, "processed": True}
   ```

2. Add the tool to the agent's tools list:
   ```python
   root_agent = Agent(
       name="it_office_agent",
       model=os.getenv("ADK_MODEL", "gemini-2.0-flash"),
       description="Manage products, stock, orders, returns & reports for ecommerce shops.",
       instruction="You are a helpful IT‑Office agent for ecommerce operations.",
       tools=[list_products, update_stock, process_order, get_sales_report, get_current_time, process_return],
   )
   ```

### Creating a New Sub-Agent for the YouTube Shorts System

To add a new sub-agent to the YouTube Shorts system:

1. Define the new agent:
   ```python
   trending_topics_agent = LlmAgent(
       name="trending_topics_agent",
       model="gemini-2.0-flash",
       instruction="Research and identify trending topics related to the user's query that would make engaging YouTube Shorts content.",
       tools=[google_search],
       output_key="trending_topics",  # Save result to state
   )
   ```

2. Add the new agent to the YouTube Shorts agent's sub-agents list:
   ```python
   youtube_shorts_agent = LlmAgent(
       name="youtube_shorts_agent",
       model="gemini-2.5-pro-exp-03-25",
       description="You are a ShortForm Genius, an AI specialized in crafting engaging Youtube Shorts content.",
       instruction=load_instruction_from_file("shorts_agent_instruction.txt"),
       sub_agents=[trending_topics_agent,  # New agent added first
                   script_writer_agent,
                   visual_editor_agent,
                   formatter_agent
                   ]
   )
   ```

