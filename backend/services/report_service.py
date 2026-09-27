# Report Service
import asyncio
import httpx
from config import Config
from . import cerebras_service
from . import llama_service

async def generate_summary(text: str) -> str:
    """
    Generate a summary of legal text using Llama AI.
    """
    # Use Llama service for summarization
    summary_result = await llama_service.summarize_and_score(text)
    return summary_result.get("summary", "Summary not available")

async def generate_report(analysis: str) -> str:
    """
    Generate a full report based on analysis.
    """
    # In a real implementation, you would generate a detailed report
    # For now, return a mock response
    report = f"Full Legal Report:\n\n{analysis}\n\n"
    report += "Detailed findings and recommendations have been prepared."
    
    return report

# New function to generate a comprehensive analysis with risk scoring
async def generate_comprehensive_analysis(text: str) -> dict:
    """
    Generate a comprehensive analysis including summary, risk scoring, and recommendations.
    """
    # Use Llama service for comprehensive analysis
    analysis_result = await llama_service.summarize_and_score(text)
    
    # Add additional analysis from Cerebras if needed
    cerebras_analysis = await cerebras_service.analyze_contract(text)
    
    analysis_result["cerebras_insights"] = str(cerebras_analysis)
    
    return analysis_result