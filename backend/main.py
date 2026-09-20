from pathlib import Path
import re

import torch
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "classifier_clean"

FRONTEND_DIR = BASE_DIR / "frontend"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH
)

model.eval()


app = FastAPI(
    title="News Classification API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class NewsRequest(BaseModel):
    text: str



def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"[^a-z0-9\s.,!?'-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# -----------------------------
# Home endpoint
# -----------------------------

@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")



@app.post("/predict")
def predict_news(request: NewsRequest):

    cleaned_text = clean_text(request.text)

    inputs = tokenizer(
        cleaned_text,
        return_tensors="pt",
        truncation=True,
        max_length=128
    )

    with torch.no_grad():
        outputs = model(**inputs)

        probabilities = torch.softmax(
            outputs.logits,
            dim=-1
        )[0]

    prediction = torch.argmax(
        probabilities
    ).item()

    classes = {
        0: "Business",
        1: "Sports",
        2: "Technology"
    }

    return {
        "text": request.text,
        "category": classes[prediction],
        "probabilities": {
            "Business": round(probabilities[0].item() * 100, 2),
            "Sports": round(probabilities[1].item() * 100, 2),
            "Technology": round(probabilities[2].item() * 100, 2)
        }
    }

app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)