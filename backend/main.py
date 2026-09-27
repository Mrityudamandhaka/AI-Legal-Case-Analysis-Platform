# FastAPI app
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import traceback

print("Starting LawMind Backend...")

try:
    from routes import upload, analyze, summarize, extract, auth
    print("All routes imported successfully")
except Exception as e:
    print(f"Error importing routes: {e}")
    traceback.print_exc()
    sys.exit(1)

app = FastAPI(title="LawMind Backend")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from the frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router)
app.include_router(analyze.router)
app.include_router(summarize.router)
app.include_router(extract.router)
app.include_router(auth.router)

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "LawMind Backend API is running"}

# New endpoint for comprehensive analysis
@app.post("/comprehensive-analysis")
async def comprehensive_analysis(request: dict):
    text = request.get("text", "")
    if not text:
        return {"error": "No text provided"}
    
    try:
        from services import report_service
        analysis = await report_service.generate_comprehensive_analysis(text)
        return {"message": "Comprehensive analysis completed", "analysis": analysis}
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    print("Starting Uvicorn server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)