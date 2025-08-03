from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class ClientCreate(BaseModel):
    name: str = Field(..., description="The full name of the client.")
    email: EmailStr = Field(..., description="The email address of the client.")
    phone: str = Field(..., description="The phone number of the client.")

class OrderCreate(BaseModel):
    client_name: str = Field(..., description="The name of the client for whom the order is being created.")
    course_name: str = Field(..., description="The name of the course the client is ordering.")

class APIResponse(BaseModel):
    message: str = Field(..., description="A message describing the result of the operation.")
    data: Optional[Dict[str, Any]] = Field(None, description="The data returned by the operation, if any.")
    cached: Optional[bool] = Field(None, description="Indicates if the response was served from cache.")


class AgentResponseData(BaseModel):
    agent_response: Any = Field(..., description="The raw response from the agent.")

class AgentAPIResponse(APIResponse):
    data: AgentResponseData