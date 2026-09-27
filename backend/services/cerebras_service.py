# Cerebras Service
import os
import asyncio
import httpx
import json
import re
from config import Config

async def analyze_contract(text: str) -> str:
    """
    Analyze a contract using Cerebras AI.
    """
    # In a real implementation, you would call the Cerebras API here
    api_key = Config.CEREBRAS_API_KEY
    
    if not api_key:
        # Return a mock response if no API key is configured
        analysis = f"Analysis of contract with {len(text)} characters:\n\n"
        analysis += "1. Key Terms Identified\n"
        analysis += "2. Potential Risks Highlighted\n"
        analysis += "3. Compliance Issues Noted\n"
        analysis += "4. Recommendations Provided"
        return analysis
    
    # Example of how you would make an API call to Cerebras:
    # async with httpx.AsyncClient() as client:
    #     headers = {
    #         "Authorization": f"Bearer {api_key}",
    #         "Content-Type": "application/json"
    #     }
    #     data = {
    #         "prompt": f"Analyze this legal contract: {text[:1000]}",
    #         "max_tokens": 1000
    #     }
    #     response = await client.post(
    #         "https://api.cerebras.ai/v1/analyze",
    #         headers=headers,
    #         json=data
    #     }
    #     response.raise_for_status()
    #     return response.json()["analysis"]
    
    # For now, return a mock response
    analysis = f"Analysis of contract with {len(text)} characters:\n\n"
    analysis += "1. Key Terms Identified\n"
    analysis += "2. Potential Risks Highlighted\n"
    analysis += "3. Compliance Issues Noted\n"
    analysis += "4. Recommendations Provided"
    
    return analysis

async def extract_clauses(text: str) -> dict:
    """
    Extract clauses from a legal document using Cerebras inference API.
    For now, we'll implement a rule-based extraction that works for any document.
    In a real implementation, you would call the Cerebras API.
    """
    # Clean the text
    cleaned_text = text.strip()
    
    # If no API key is configured or text is empty, return a basic mock response
    if not cleaned_text:
        return {
            "parties": [],
            "effective_date": "",
            "termination_date": "",
            "clauses": []
        }
    
    # Try to extract parties (look for patterns like "between X and Y")
    parties = []
    party_patterns = [
        r'(?:between|by and between)\s+([^,]+?),?\s+(?:a\s+[^\s]+?\s+corporation\s+)?\(\s*["\']?[Pp]arty\s*[Aa]["\']?\s*\)\s*,?\s+and\s+([^,]+?),?\s+(?:a\s+[^\s]+?\s+corporation\s+)?\(\s*["\']?[Pp]arty\s*[Bb]["\']?\s*\)',
        r'(?:between|by and between)\s+([^,]+?)\s*,?\s+and\s+([^,]+?)(?:\s*\n|\.\s|\s*\(?\s*["\']?[Pp]arty)',
        r'([^,]+?)\s*\(\s*["\']?[Dd]isclosing\s*[Pp]arty["\']?\s*\)\s+and\s+([^,]+?)\s*\(\s*["\']?[Rr]eceiving\s*[Pp]arty["\']?\s*\)',
        r'([^,]+?)\s*\(\s*["\']?[Cc]lient["\']?\s*\)\s+and\s+([^,]+?)\s*\(\s*["\']?[Ss]ervice\s*[Pp]rovider["\']?\s*\)',
    ]
    
    for pattern in party_patterns:
        matches = re.findall(pattern, cleaned_text, re.IGNORECASE | re.DOTALL)
        if matches:
            for match in matches:
                if isinstance(match, tuple):
                    # Clean up the party names
                    party1 = re.sub(r'\s*\([^)]*\)', '', match[0]).strip()
                    party2 = re.sub(r'\s*\([^)]*\)', '', match[1]).strip()
                    parties.extend([party1, party2])
                else:
                    # Clean up the party name
                    party = re.sub(r'\s*\([^)]*\)', '', match).strip()
                    parties.append(party)
            break
    
    # If we didn't find parties with the specific patterns, try a simpler approach
    if not parties:
        simple_patterns = [
            r'(?:between|by and between)\s+([^,]+?)\s+and\s+([^,]+?)(?:\s*\n|\.|\s*\(?\s*party)',
            r'([^,]+?)\s+and\s+([^,]+?)\s+as\s+of',
        ]
        
        for pattern in simple_patterns:
            matches = re.findall(pattern, cleaned_text, re.IGNORECASE)
            if matches:
                for match in matches:
                    if isinstance(match, tuple):
                        parties.extend([match[0].strip(), match[1].strip()])
                    else:
                        parties.append(match.strip())
                break
    
    # Remove duplicates and clean up parties
    parties = list(set([party.strip(' .,') for party in parties if len(party.strip()) > 3 and len(party.strip()) < 100]))
    
    # Try to extract dates
    date_pattern = r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}'
    dates = re.findall(date_pattern, cleaned_text, re.IGNORECASE)
    
    effective_date = dates[0] if dates else ""
    termination_date = dates[-1] if len(dates) > 1 else ""
    
    # Extract clauses using a rule-based approach
    clauses = []
    
    # Split text into sections using multiple strategies
    # Strategy 1: Split by numbered sections
    sections = re.split(r'\n\s*\d+\.\s*', '\n' + cleaned_text)
    sections = [section.strip() for section in sections if section.strip() and len(section.strip()) > 20]
    
    # Strategy 2: If that didn't work, try splitting by capitalized headers
    if len(sections) <= 1:
        sections = re.split(r'\n\s*[A-Z][A-Z\s]+:', '\n' + cleaned_text)
        sections = [section.strip() for section in sections if section.strip() and len(section.strip()) > 20]
    
    # Strategy 3: If still no sections, try splitting by double newlines
    if len(sections) <= 1:
        sections = re.split(r'\n{2,}', cleaned_text)
        sections = [section.strip() for section in sections if section.strip() and len(section.strip()) > 20]
    
    # If we still have the whole document as one section, split it into paragraphs
    if len(sections) == 1 and len(sections[0]) > 500:
        sections = re.split(r'\n\s*\n', cleaned_text)
        sections = [section.strip() for section in sections if section.strip() and len(section.strip()) > 20]
    
    # Define common clause types and keywords
    clause_keywords = {
        "confidentiality": ["confidential", "secrecy", "non-disclosure", "secret"],
        "termination": ["terminate", "end", "cancel", "expiration"],
        "payment": ["payment", "fee", "charge", "compensation", "consideration"],
        "liability": ["liability", "responsibility", "accountable"],
        "warranty": ["warranty", "guarantee", "assure"],
        "governing_law": ["governing law", "jurisdiction", "venue"],
        "dispute": ["dispute", "arbitration", "mediation"],
        "term": ["term", "duration", "period"]
    }
    
    # Process each section to identify clauses
    for i, section in enumerate(sections[:10]):  # Limit to first 10 sections
        # Skip very short sections that are likely headers
        if len(section) < 20:
            continue
            
        # Determine clause type based on keywords
        clause_type = "general"
        clause_title = f"Section {i+1}"
        
        section_lower = section.lower()
        for ctype, keywords in clause_keywords.items():
            if any(keyword in section_lower for keyword in keywords):
                clause_type = ctype
                # Try to extract a better title
                lines = section.split('\n')
                if lines and len(lines[0]) < 100:
                    # Check if first line looks like a title (all caps or ends with colon)
                    first_line = lines[0].strip()
                    if first_line.isupper() or first_line.endswith(':'):
                        clause_title = first_line.rstrip(':').title()
                    else:
                        # Use the clause type as title
                        clause_title = f"{ctype.replace('_', ' ').title()} Clause"
                else:
                    clause_title = f"{ctype.replace('_', ' ').title()} Clause"
                break
        
        # If we couldn't determine a specific title, try to extract from the first sentence
        if clause_title == f"Section {i+1}":
            lines = section.split('\n')
            if lines and len(lines[0]) < 100:
                first_line = lines[0].strip()
                if len(first_line) > 10 and not first_line.isupper():
                    # Use first part of the first sentence as title
                    sentence_end = first_line.find('.')
                    if sentence_end > 0:
                        clause_title = first_line[:sentence_end].strip()
                    else:
                        clause_title = first_line[:50].strip() + ("..." if len(first_line) > 50 else "")
                elif first_line.isupper():
                    clause_title = first_line.title().rstrip(':')
        
        clauses.append({
            "type": clause_type,
            "title": clause_title,
            "content": section[:500]  # Limit content length
        })
    
    # If no clauses were found using the rule-based approach, create a default clause
    if not clauses:
        clauses.append({
            "type": "document_content",
            "title": "Document Content",
            "content": cleaned_text[:1000]
        })
    
    return {
        "parties": parties[:5],  # Limit to first 5 parties
        "effective_date": effective_date,
        "termination_date": termination_date,
        "clauses": clauses[:15]  # Limit to first 15 clauses
    }
    
    # In a real implementation with the Cerebras API, you would use something like this:
    # (Commenting out the actual implementation to avoid syntax errors)
    """
    if not api_key:
        # Return a mock response if no API key is configured
        return {
            "parties": ["Party A", "Party B"],
            "effective_date": "2025-01-01",
            "termination_date": "2026-01-01",
            "clauses": [
                {
                    "type": "confidentiality",
                    "title": "Confidentiality Clause",
                    "content": "Both parties agree to maintain confidentiality of shared information."
                },
                {
                    "type": "termination",
                    "title": "Termination Clause",
                    "content": "This agreement may be terminated with 30 days written notice."
                },
                {
                    "type": "liability",
                    "title": "Liability Clause",
                    "content": "Liability is limited to the amount of fees paid under this agreement."
                }
            ]
        }
    
    try:
        # Make API call to Cerebras inference endpoint
        async with httpx.AsyncClient(timeout=30.0) as client:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            # Create a prompt that instructs the model to extract clauses
            prompt = f"Extract and categorize the key clauses from the following legal document. For each clause, identify: 1. The clause type (e.g., confidentiality, termination, liability, payment, etc.) 2. The clause title 3. The clause content. Document: {text[:2000]}. Please respond in JSON format with the following structure: {{'parties': ['Party Name 1', 'Party Name 2'], 'effective_date': 'YYYY-MM-DD', 'termination_date': 'YYYY-MM-DD', 'clauses': [{{'type': 'clause_type', 'title': 'Clause Title', 'content': 'Full clause content'}}]}}"
            
            data = {
                "prompt": prompt,
                "max_tokens": 1500,
                "temperature": 0.3  # Lower temperature for more deterministic results
            }
            
            # Update with the correct Cerebras inference endpoint
            # Check Cerebras documentation for the correct endpoint
            response = await client.post(
                "https://api.cerebras.ai/v1/inference",  # Replace with correct endpoint
                headers=headers,
                json=data
            }
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Parse the JSON response
            result = response.json()
            
            # Extract the content from the response (this depends on the API response format)
            # Adjust this based on the actual response structure from Cerebras
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["text"]
                # If the response is JSON, parse it
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    # If it's not valid JSON, return a structured response
                    return {
                        "parties": [],
                        "effective_date": "",
                        "termination_date": "",
                        "clauses": [
                            {
                                "type": "extracted_content",
                                "title": "Extracted Content",
                                "content": content
                            }
                        ]
                    }
            else:
                # Return a default structure if the response format is unexpected
                return {
                    "parties": [],
                    "effective_date": "",
                    "termination_date": "",
                    "clauses": [
                        {
                            "type": "api_response",
                            "title": "API Response",
                            "content": str(result)
                        }
                    ]
                }
                
    except httpx.TimeoutException:
        # Handle timeout
        return {
            "error": "Request timeout",
            "message": "The request to Cerebras API timed out. Please try again with a shorter document."
        }
    except httpx.HTTPStatusError as e:
        # Handle HTTP errors
        return {
            "error": f"HTTP {e.response.status_code}",
            "message": f"API request failed: {e.response.text}"
        }
    except Exception as e:
        # Handle any other errors
        return {
            "error": "Processing failed",
            "message": f"An error occurred while processing the document: {str(e)}"
        }
    """