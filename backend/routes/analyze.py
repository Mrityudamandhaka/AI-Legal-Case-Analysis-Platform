from fastapi import APIRouter, HTTPException, Depends
from services import cerebras_service, llama_service
from services.auth_service import get_current_user

router = APIRouter(prefix="/analyze", tags=["analyze"])

@router.post("/")
async def analyze_document(request: dict, current_user = Depends(get_current_user)):
    text = request.get("text", "")
    print(f"User {current_user.username} analyzing document")
    
    if not text:
        raise HTTPException(status_code=400, detail="No text provided for analysis")
    
    try:
        # Use Cerebras service for analysis
        analysis = await cerebras_service.analyze_contract(text)
        return {"message": "Document analyzed successfully", "analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during analysis: {str(e)}")