import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Configure the Gemini API key
genai.configure(api_key="AIzaSyAiSeon2RzZZrJPy2EM2yNGALy61siYBO4")

# Create FastAPI app instance
app = FastAPI()

# Pydantic model for input data validation
class MitigationRequest(BaseModel):
    topics: dict  # A dictionary of topic:value pairs

# Function to query LLM for mitigation strategies
def get_mitigation_solution(input_value: str):
    prompt = f"Given the following input: {input_value}, provide mitigation strategies."
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.candidates[0].content.parts[0].text

# FastAPI route for the mitigation endpoint
@app.post("/api/mitigation")
async def mitigation(request: MitigationRequest):
    results = {}
    try:
        for topic, input_value in request.topics.items():
            # Get mitigation strategy from LLM based on input value
            solution = get_mitigation_solution(input_value)
            results[topic] = {
                "mitigation_solution": solution
            }
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
