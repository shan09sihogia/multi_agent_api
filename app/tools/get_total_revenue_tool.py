from crewai.tools import tool
from app.services.mongodb_tool import MongoDBTool

@tool("Get Total Revenue This Month")
def get_total_revenue_this_month_tool() -> float:
    """
    Useful for calculating the total revenue generated from all completed payments this current month.
    Returns the total revenue as a numerical value (float).
    """

    return MongoDBTool().get_total_revenue_this_month()