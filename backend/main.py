"""
AI IDE Assistant — Backend
FastAPI server serving CodeBERT-based Java code completions.

Tools used:
  • FastAPI        — high-performance async REST API framework
  • Pydantic v2    — request/response validation
  • HuggingFace Transformers — CodeBERT model loading & tokenisation
  • PyTorch        — model inference (CPU)
  • Uvicorn        — ASGI server

Author: Naram Prashanth Goud
GitHub: https://github.com/prashanth9968
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoTokenizer, AutoModelForMaskedLM
import torch

app = FastAPI(
    title="AI IDE Assistant API",
    description="Real-time Java code completion using Microsoft CodeBERT",
    version="1.0.0",
)

# Allow VS Code extension (localhost) to call the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Load CodeBERT ──────────────────────────────────────────────────────────────
# First run: ~500 MB downloaded from HuggingFace and cached locally.
# Subsequent runs: loaded from cache (fast).
# ──────────────────────────────────────────────────────────────────────────────
MODEL_NAME = "microsoft/codebert-base"
print(f"Loading {MODEL_NAME} ...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model     = AutoModelForMaskedLM.from_pretrained(MODEL_NAME)
model.eval()   # inference mode — disables dropout
print("Model ready ✅")


# ── Request / Response schemas ─────────────────────────────────────────────────
class CodeRequest(BaseModel):
    code: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "code": "public class Hello { public static void main(String[] args) {"
            }
        }
    }


class CompletionResponse(BaseModel):
    completion: str


# ── Endpoints ──────────────────────────────────────────────────────────────────
@app.get("/", summary="Health check")
def root():
    """Confirms the backend is running."""
    return {"message": "AI IDE Assistant Backend Running", "status": "ok"}


@app.post("/complete", response_model=CompletionResponse, summary="Get next-token suggestion")
def complete_code(request: CodeRequest):
    """
    Accepts the code written before the cursor and returns the AI-predicted next token.

    Algorithm:
      1. Append [MASK] to the code snippet.
      2. Tokenise (truncate from the left to keep the most recent context within 512 tokens).
      3. Run CodeBERT forward pass.
      4. Argmax over [MASK] logits → decode → return.
    """
    code = request.code.strip()
    if not code:
        raise HTTPException(status_code=400, detail="Code input cannot be empty.")

    masked_code = code + " " + tokenizer.mask_token

    inputs = tokenizer(
        masked_code,
        return_tensors="pt",
        truncation=True,
        max_length=512,
        padding=False,
    )

    with torch.no_grad():
        outputs = model(**inputs)

    mask_positions = torch.where(inputs["input_ids"] == tokenizer.mask_token_id)[1]
    if mask_positions.numel() == 0:
        raise HTTPException(status_code=422, detail="Could not locate [MASK] token in tokenised input.")

    predicted_id    = outputs.logits[0, mask_positions].argmax(dim=-1)
    predicted_token = tokenizer.decode(predicted_id).strip()

    return CompletionResponse(completion=" " + predicted_token)
