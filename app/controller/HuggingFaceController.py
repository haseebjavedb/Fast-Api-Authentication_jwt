from huggingface_hub import InferenceClient
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import json
import os
from dotenv import load_dotenv

load_dotenv()  

HuggingFaceRouter = APIRouter()

hf_token = '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'
bot_id = 'microsoft/Phi-3-mini-4k-instruct'



def get_llm_client():
    return InferenceClient(model=bot_id, token=hf_token, timeout=120)

class PromptRequest(BaseModel):
    prompt: str

@HuggingFaceRouter.post("/HuggingFaceModel/")
async def call_llm(request: PromptRequest, llm_client: InferenceClient = Depends(get_llm_client)):
    try:
        response = llm_client.post(
            json={
                "inputs": request.prompt,
                "parameters": {"max_new_tokens": 200},
                "task": "text-generation",
            }
        )
        generated_text = json.loads(response.decode())[0]["generated_text"]
        return {"response": generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
