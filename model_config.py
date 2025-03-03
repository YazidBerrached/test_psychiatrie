import nest_asyncio
nest_asyncio.apply()
from pydantic_ai.models.openai import OpenAIModel
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from pydantic_ai.models.groq import GroqModel
import os
from dotenv import load_dotenv
load_dotenv()


embedding_model = SentenceTransformer("BAAI/bge-small-en-v1.5")

def get_embedding(text: str):
    return embedding_model.encode(text)

# Fonction pour calculer la similarité cosine
def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

## initialer le user ID pour le TEST
user_email=  0
system_prompt_master = ""
is_starting = False

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
model = OpenAIModel('gpt-4o', api_key=OPENAI_API_KEY)
# GROQ_API_KEY = "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"
# model = GroqModel('llama-3.3-70b-versatile', api_key=GROQ_API_KEY)