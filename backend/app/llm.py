import os 
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
# print("GROQ_API:", os.getenv("GROQ_API_KEY"))

def extract_action_items(transcript:str):
    prompt=f"""
    You are an AI assistant that extracts action items from meeting transcripts.

    CRITICAL EXTRACTION RULES:

    1. Distinguish clearly between the SPEAKER and the ASSIGNEE.
    2. Do NOT assume "I", "me", or "we" refers to the assignee.
    3. Split multiple actions into separate tasks.
    4. If a task uses phrases like "ask X to do Y":
    - assign the task to X
    - the task is Y
    - do NOT create a task for the person who is asking
    5. Do NOT assign tasks to abstract entities.
    6. If assignee cannot be determined, set assigned_to_name = "Unassigned".
    7. Merge repeated or semantically similar tasks.
    8. Preserve deadlines exactly as mentioned.
    9. Do NOT invent tasks.
    10. Return ONLY valid JSON.



    Return ONLY valid JSON in the following format:

    [
    {{
        "task": "string",
        "assigned_to_name": "string or null",
        "due_text": "string or null",
        "confidence_score": float
    }}
    ]

    Transcript:
    {transcript}

    """


    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role":"system", "content": "You are a helpful assistant."},
            {"role":"user", "content":prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


import json

def parse_llm_response(raw_output):
    # CASE 1: Already parsed (list)
    if isinstance(raw_output, list):
        return raw_output

    # CASE 2: JSON string
    if isinstance(raw_output, str):
        try:
            return json.loads(raw_output)
        except Exception as e:
            print("Json parse failed")
            print("Raw llm output", raw_output)
            return []

    # CASE 3: Anything else
    return []
