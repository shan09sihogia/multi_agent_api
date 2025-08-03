from crewai.tools import tool
from typing import Optional
from app.services.mongodb_tool import MongoDBTool

@tool("Get Order Details By Client")
def get_order_details_by_client_tool(client_query: str, status: Optional[str] = None) -> list:
    """
    Useful for finding orders associated with a specific client by their name, email, or phone number.
    Optionally filters orders by status (e.g., 'paid', 'pending').

    Args:
        client_query (str): The client's name, email, or phone number (e.g., 'Priya Sharma').
        status (Optional[str]): Optional: Filter orders by status (e.g., 'paid', 'pending').

    Returns:
        list: A list of matching orders.
    """
  
    return MongoDBTool().get_order_details_by_client(client_query=client_query, status=status)