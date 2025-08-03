from crewai.tools import tool
from app.services.mongodb_tool import MongoDBTool

@tool("Get Enrollment Trends")
def get_enrollment_trends_tool() -> list:
    """
    Useful for providing insights into course enrollment trends, showing which courses have the most enrollments.
    Returns a list of courses and their enrollment counts, sorted by popularity.
    """

    return MongoDBTool().get_enrollment_trends()