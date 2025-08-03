from crewai.tools import tool
from typing import Optional
from app.services.mongodb_tool import MongoDBTool

@tool("Get Attendance Percentage By Class")
def get_attendance_percentage_by_class_tool(course_name: Optional[str] = None) -> dict:
    """
    Useful for calculating the attendance percentage for specific classes or all classes.
    Optionally filtered by course name.
    If 'course_name' is provided, returns attendance percentage for classes within that course.
    If 'course_name' is omitted, returns attendance percentage for all classes.
    Returns a dictionary of attendance percentages for each class.
    """
 
    return MongoDBTool().get_attendance_percentage_by_class(course_name=course_name)