from fastapi import APIRouter, Header, Depends, HTTPException, status
from app.agents.support_agent import SupportAgent
from app.agents.dashboard_agent import DashboardAgent
from app.models.common import AgentAPIResponse, AgentResponseData # Import specific response model

router = APIRouter()


def get_support_agent_instance() -> SupportAgent:
    """Provides a SupportAgent instance."""
    return SupportAgent()


def get_dashboard_agent_instance() -> DashboardAgent:
    """Provides a DashboardAgent instance."""
    return DashboardAgent()

@router.get(
    "/support/query",
    response_model=AgentAPIResponse,
    summary="Query the Support Agent",
    description="Sends a natural language query to the Support Agent. The agent can answer questions about courses, orders, payments, and clients. It also supports creating clients and orders."
)
async def support_query(
    q: str,
    session_id: str = Header("global", description="Optional: Session ID for memory/caching. Defaults to 'global'."),
    support_agent: SupportAgent = Depends(get_support_agent_instance)
):
    """
    Handles natural language queries for the Support Agent.
    """
    try:
        result = support_agent.run(q, session_id)
        return AgentAPIResponse(
            message="Query processed successfully by Support Agent.",
            data=AgentResponseData(agent_response=result["response"]),
            cached=result["cached"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing support query: {e}"
        )

@router.get(
    "/dashboard/query",
    response_model=AgentAPIResponse,
    summary="Query the Dashboard Agent",
    description="Sends a natural language query to the Dashboard Agent. The agent can provide analytics and metrics useful for business owners, such as revenue, client insights, service analytics, and attendance reports. [cite: 40]"
)
async def dashboard_query(
    q: str,
    dashboard_agent: DashboardAgent = Depends(get_dashboard_agent_instance) 
):
    """
    Handles natural language queries for the Dashboard Agent.
    """
    try:
        result = dashboard_agent.run(q)
        
        return AgentAPIResponse(
            message="Query processed successfully by Dashboard Agent.",
            data=AgentResponseData(agent_response=result),
            cached=False
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing dashboard query: {e}"
        )