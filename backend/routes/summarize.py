from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from services import llama_service
from services.auth_service import get_current_user
import json

router = APIRouter(prefix="/summarize", tags=["summarize"])

class SummarizeRequest(BaseModel):
    text: str

class SummarizeResponse(BaseModel):
    message: str
    summary: str
    risk_score: int
    risk_level: str
    key_points: list
    recommendations: list

@router.post("/", response_model=SummarizeResponse)
async def summarize_document(request: SummarizeRequest, current_user = Depends(get_current_user)):
    print(f"User {current_user.username} summarizing document")
    
    if not request.text:
        raise HTTPException(status_code=400, detail="No text provided for summarization")
    
    try:
        # Use Llama service for summarization and risk scoring
        summary_result = await llama_service.summarize_and_score_real(request.text)
        
        # Ensure all required fields are present
        response_data = {
            "message": "Document summarized successfully",
            "summary": summary_result.get("summary", "Summary not available"),
            "risk_score": summary_result.get("risk_score", 50),
            "risk_level": summary_result.get("risk_level", "Medium"),
            "key_points": summary_result.get("key_points", ["No key points extracted"]),
            "recommendations": summary_result.get("recommendations", ["No recommendations provided"])
        }
        
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during summarization: {str(e)}")