from crewai.tools import tool
from app.services.mongodb_tool import MongoDBTool

@tool("Get Course Completion Rates")
def get_course_completion_rates_tool() -> dict:
    """
    Useful for getting an approximate completion rate for courses, indicating how many orders
    for a course have been marked as completed (paid).
    Returns a dictionary of courses and their completion percentages.
    """

    return MongoDBTool().get_course_completion_rates()