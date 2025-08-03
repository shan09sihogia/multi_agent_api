from fastapi import APIRouter, Depends, HTTPException, status
from app.services.external_api import ExternalAPI
from app.models.common import ClientCreate, OrderCreate, APIResponse 

router = APIRouter()

def get_external_api_instance() -> ExternalAPI:
    """Provides an ExternalAPI instance."""
    return ExternalAPI()

@router.post(
    "/client",
    response_model=APIResponse,
    summary="Create a new client",
    description="Creates a new client record in the database."
)
async def create_client(
    data: ClientCreate, 
    api: ExternalAPI = Depends(get_external_api_instance) 
):
    """
    Endpoint to create a new client.
    """
    try:
        result = api.create_client(data)
        return APIResponse(message="Client created successfully.", data=result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating client: {e}"
        )

@router.post(
    "/order",
    response_model=APIResponse,
    summary="Create a new order",
    description="Creates a new order in the database for a specified client and course. [cite: 33]"
)
async def create_order(
    data: OrderCreate,
    api: ExternalAPI = Depends(get_external_api_instance) 
):
    """
    Endpoint to create a new order.
    """
    try:
        result = api.create_order(data)
        if "error" in result:
             raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=result["error"]
            )
        return APIResponse(message="Order created successfully.", data=result)
    except HTTPException as http_exc:
        raise http_exc 
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating order: {e}"
        )