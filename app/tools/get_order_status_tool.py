from crewai.tools import tool
from app.services.mongodb_tool import MongoDBTool

@tool("Get Order Status")
def get_order_status_tool(order_id: int) -> str:
    """
    Useful for fetching the current status of an order by its numerical ID 
    (e.g., 'Has order #12345 been paid?'). 
    Returns the status (e.g., 'pending', 'paid', or 'not found').
    """
    return MongoDBTool().get_order_status(order_id)

