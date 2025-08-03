from crewai.tools import tool
from app.services.mongodb_tool import MongoDBTool

@tool("Filter Upcoming Classes")
def filter_classes_tool(query: str) -> list:
    """
    Useful for filtering upcoming classes by a specific instructor or course name.
    Use this when the user asks for classes by a specific instructor or course
    (e.g., 'List yoga classes by Anjali' or 'Show upcoming Pilates classes').
    The input should be a keyword to filter upcoming classes by instructor name or course name (e.g., 'Anjali' or 'Yoga').
    Returns a list of filtered classes.
    """
    return MongoDBTool().filter_classes(query=query)