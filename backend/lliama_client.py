# llama_client.py
import os
from openai import OpenAI

# Together.ai API endpoint (Llama 3 hosted)
client = OpenAI(
    api_key=os.getenv("TOGETHER_API_KEY"),
    base_url="https://api.together.xyz/v1"
)

def summarize_clause(clause_text):
    """Summarize a legal clause in simple English."""
    prompt = f"""
    You are a legal AI assistant. 
    Read the clause below and summarize it in 2–3 sentences 
    in plain English for a non-lawyer.

    Clause:
    {clause_text}
    """

    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.4,
    )
    return response.choices[0].message.content.strip()


def assess_risk(clause_text):
    """Analyze clause and assign risk level."""
    prompt = f"""
    You are a legal risk analyst AI.
    Analyze the clause below and assign a risk level: Low, Medium, or High.
    Justify in 1 sentence.

    Clause:
    {clause_text}

    Respond in JSON:
    {{
        "risk_level": "<Low/Medium/High>",
        "justification": "<reason>"
    }}
    """

    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()
