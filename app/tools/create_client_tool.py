from crewai.tools import tool
from pydantic import EmailStr
from app.services.external_api import ExternalAPI
from app.models.common import ClientCreate

@tool("Create Client")
def create_client_tool(name: str, email: EmailStr, phone: str) -> dict:
    """
    Useful for creating a new client enquiry or registering a new client in the system.
    Requires the client's name, email, and phone number.
    Example: 'Register a new client named John Doe with email john@example.com and phone 1234567890'.
    """
    client_data = ClientCreate(name=name, email=email, phone=phone)

    return ExternalAPI().create_client(client_data)