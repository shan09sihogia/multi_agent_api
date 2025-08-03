from crewai.tools import tool
from typing import Optional
from app.services.mongodb_tool import MongoDBTool

@tool("Get Top Services")
def get_top_services_tool(limit: Optional[int] = 3) -> list:
    """
    Useful for identifying the most popular courses/services based on enrollment numbers.
    Optionally specify a 'limit' to control the maximum number of top services to return.
    If 'limit' is omitted, it defaults to 3.
    Returns a list of the most popular services.
    """
  
    return MongoDBTool().get_top_services(limit=limit)