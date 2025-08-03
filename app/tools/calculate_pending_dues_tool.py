from crewai.tools import tool
from app.services.mongodb_tool import MongoDBTool

@tool("Calculate Pending Dues")
def calculate_pending_dues_tool(client_query: str) -> str:
    """
    Useful for calculating the total amount of pending payments for a specific client. 
    The input should be the client's name, email, or phone number to calculate their pending dues.
    Returns the client's name and total pending dues.
    """
  
    return MongoDBTool().calculate_pending_dues(client_query)

