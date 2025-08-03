from crewai.tools import tool
from app.services.mongodb_tool import MongoDBTool

@tool("Get Payment Details For Order")
def get_payment_details_for_order_tool(order_id: int) -> dict | None:
    """
    Useful for retrieving all payment details (amount, date, status) associated with a specific order ID.
    The input should be the numerical ID of the order to retrieve payment details for (e.g., 'What are the payment details for order 54321?').
    Returns a dictionary with payment details if found, otherwise None.
    """

    return MongoDBTool().get_payment_details_for_order(order_id)