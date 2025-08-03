import os
from crewai import Agent, Task, Crew , LLM

from app.tools.get_total_revenue_tool import get_total_revenue_this_month_tool
from app.tools.get_outstanding_payments_tool import get_outstanding_payments_tool
from app.tools.get_active_inactive_clients_tool import get_active_inactive_clients_count_tool
from app.tools.get_new_clients_this_month_tool import get_new_clients_this_month_tool
from app.tools.get_enrollment_trends_tool import get_enrollment_trends_tool
from app.tools.get_top_services_tool import get_top_services_tool
from app.tools.get_course_completion_rates_tool import get_course_completion_rates_tool
from app.tools.get_attendance_percentage_by_class_tool import get_attendance_percentage_by_class_tool

from app.core.config import GEMINI_API_KEY 


class DashboardAgent:
    def __init__(self):
        direct_llm = LLM(
            model="gemini/gemini-2.5-pro",
            api_key=GEMINI_API_KEY,
    
        )
        self.agent = Agent(
            role="Dashboard Analytics Bot",
            goal="Provide accurate and insightful analytics and metrics useful for business owners, covering revenue, client insights, service analytics, and attendance reports.",
            tools=[
                get_total_revenue_this_month_tool,
                get_outstanding_payments_tool,
                get_active_inactive_clients_count_tool,
                get_new_clients_this_month_tool,
                get_enrollment_trends_tool,
                get_top_services_tool,
                get_course_completion_rates_tool,
                get_attendance_percentage_by_class_tool,
            ],
            llm=direct_llm, 
            verbose=True,
            allow_delegation=False,
            backstory=(
                "You are an expert AI analyst providing key business metrics and insights from the MongoDB database. "
                "Your primary function is to interpret requests for analytics and generate detailed reports using the available tools. "
                "You can generate reports on total revenue, outstanding payments, client engagement (active/inactive, new clients), "
                "service popularity, enrollment trends, and class attendance percentages."
            )
        )

    def run(self, prompt: str):
    
        print(f"Running Dashboard Agent for prompt: '{prompt}'...")

        task = Task(
            description=prompt,
            agent=self.agent,
            expected_output="A clear and accurate analytical report based on the query, using data from available tools."
        )

        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=True
        )

        resp = crew.kickoff()
        return resp