from fastapi import HTTPException
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from discovery_client import query_discovery

router = APIRouter()


# --- Watson Discovery Endpoints ---


@router.get("/query_discovery")
async def search_discovery(query: str, product_id: str = None):
    """Queries Watson Discovery with an optional product_id filter."""
    if query_discovery is None:
         raise HTTPException(status_code=500, detail="Watson Discovery client not initialized.")

    try:
        search_results = query_discovery(query_text=query)
        print("search_results ", search_results)
        if search_results:
            return JSONResponse(content=search_results)
        else:
            raise HTTPException(status_code=500, detail="Failed to query Watson Discovery.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during Discovery query: {e}")

