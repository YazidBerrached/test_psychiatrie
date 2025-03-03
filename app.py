import nest_asyncio
nest_asyncio.apply()
import chainlit as cl
from mistralai import Mistral
from typing import Dict, Optional,List
from pydantic import BaseModel, Field
from pydantic_ai import Agent, Tool,RunContext
from pydantic_ai.models.openai import OpenAIModel
from dataclasses import dataclass
from pydantic_ai.tools import Tool, RunContext
from datetime import datetime
import json
import sqlite3
from db_models import *
from chainlit.input_widget import Slider
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from typing import List, Tuple
from pydantic_ai.models.groq import GroqModel
import re
import tools
from start_conversation import starting_conv
from desease_exact import desease_exist
from potentiel_desease import potentiel_desease
from guest_user import guest_user

@cl.on_chat_start
def on_chat_start():
    global is_starting
    is_starting = True
    user_email = cl.user_session.get("user").identifier
    cl.user_session.set("message_history", [])
    cl.user_session.set("maladie",get_desease(user_email))
    cl.user_session.set("list_maladie",[])

@cl.oauth_callback
def oauth_callback(
  provider_id: str,
  token: str,
  raw_user_data: Dict[str, str],
  default_user: cl.User,
) -> Optional[cl.User]:
    return default_user  


@cl.on_message
async def on_message(message: cl.Message):
    global user_email 
    global is_starting

        
    user_email = cl.user_session.get("user").identifier
     # Debug
    
    mh = cl.user_session.get("message_history", [])
    if is_starting:
        pp = """
        +---------------------------+
        |                           |
        |   IS STARTING CONDITION   |
        |                           |
        +---------------------------+
        """
        print(pp)
        is_starting = False
        return await starting_conv(message.content, user_email,mh)

    else:
        maladie_exacte = get_desease(user_email)
        liste_maladie = get_maladie_potentiel(user_email)
        liste_maladie[:] = [item[0] for item in liste_maladie]
        if maladie_exacte: # prendre la piste d'un psychiatre qui connait la maladie
            return await desease_exist(maladie_exacte, message.content, user_email, mh)

        elif len(liste_maladie) > 1 and maladie_exacte=="": # prendre la piste d'un psychiatre qui a une liste de maladie potentiel
            return await potentiel_desease(message.content, user_email, liste_maladie, mh)

        else:
            return await guest_user(message.content, user_email, mh)  # for new user