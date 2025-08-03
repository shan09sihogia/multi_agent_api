from crewai.tools import tool
from app.services.mongodb_tool import MongoDBTool

@tool("List Upcoming Classes")
def list_upcoming_classes_tool() -> list:
    """
    Useful for listing all upcoming classes/services without specific filters
    (e.g., 'What classes are available this week?').
    Returns a list of classes with their course, instructor, status, and date.
    """

    return MongoDBTool().list_upcoming_classes()