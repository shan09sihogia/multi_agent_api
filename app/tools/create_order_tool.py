from crewai.tools import tool
from app.services.external_api import ExternalAPI
from app.models.common import OrderCreate

@tool("Create Order")
def create_order_tool(client_name: str, course_name: str) -> dict:
    """
    Useful for creating a new order for a specific client and course.
    Requires the client's full name and the exact course name.
    Example: 'Create an order for Yoga Beginner for client Priya Sharma'.
    Returns the ID of the newly created order.
    """
    order = OrderCreate(client_name=client_name, course_name=course_name)

    return ExternalAPI().create_order(order)