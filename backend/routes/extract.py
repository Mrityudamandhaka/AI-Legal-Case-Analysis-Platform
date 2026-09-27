from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from services import cerebras_service
from services.auth_service import get_current_user
import traceback

router = APIRouter(prefix="/extract", tags=["extract"])

class ExtractRequest(BaseModel):
    text: str

class ExtractResponse(BaseModel):
    message: str
    extracted_data: dict

@router.post("/", response_model=ExtractResponse)
async def extract_clauses(request: ExtractRequest, current_user = Depends(get_current_user)):
    """
    Extract clauses from a legal document using Cerebras inference API.
    """
    print(f"User {current_user.username} extracting clauses")
    
    if not request.text:
        raise HTTPException(status_code=400, detail="No text provided for clause extraction")
    
    try:
        # Use Cerebras service for clause extraction
        extracted_data = await cerebras_service.extract_clauses(request.text)
        
        # Check if there was an error in the extraction process
        if "error" in extracted_data:
            raise HTTPException(status_code=500, detail=extracted_data["message"])
        
        return ExtractResponse(
            message="Clauses extracted successfully",
            extracted_data=extracted_data
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in extract_clauses: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error during clause extraction: {str(e)}")