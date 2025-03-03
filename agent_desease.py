import nest_asyncio
nest_asyncio.apply()
import chainlit as cl

from typing import Dict, Optional,List
from pydantic import BaseModel, Field
from pydantic_ai import Agent, Tool,RunContext
from dataclasses import dataclass
from pydantic_ai.tools import Tool, RunContext
from datetime import datetime
import json
import sqlite3
from db_models import *

import numpy as np
import pandas as pd
from model_config import model

import re

detect_desease_agent = Agent(
    model,
    system_prompt=(
        "Tu es un expert en psychologie. Ton rôle est d'analyser les propos de l'utilisateur "
        "tu dois detecter la maladie et la retourner entre deux parenthèses."
        "exemple : ((schizophrénie))"
    ),
    result_type=str,
)



@cl.step(type="tool")
async def detecte_desease(query: str, user_email:str) -> str:
    """Retourne les préférences de l'utilisateur."""
    pp = """
    ___________________________
    |                         |
    |      desease détecté    |
    |_________________________|
    
    """
    print(pp)
    result = detect_desease_agent.run_sync(query)
    detected_event = result.data
    match = re.search(r"\(\((.*?)\)\)", detected_event)

    if match:
        extracted_text = match.group(1).lower()
        save_maladie_db(user_email,extracted_text) 
        delete_list_maladie(user_email,extracted_text)
    print("+----------------------------+")
    print("|                            |")
    print(f"|     {detected_event}      |")
    print("+----------------------------+")
    print(f"|     {extracted_text}      |")
    print("+----------------------------+")
    return detected_event


detecte_desease_tool= Tool(
    detecte_desease,
    description="Détecte la maladie en analysant les symptômes du patient."
)
