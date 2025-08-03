from crewai.tools import tool
from app.services.mongodb_tool import MongoDBTool

@tool("Get Client Enrolled Services")
def get_client_enrolled_services_tool(client_query: str) -> list:
    """
    Useful for viewing all services a client is currently enrolled in and their status (active/inactive).
    The input should be the client's name, email, or phone number to look up their enrolled services (e.g., 'Rahul Singh').
    Returns a list of enrolled services and their status for the client.
    """
    
    return MongoDBTool().get_client_enrolled_services(client_query)