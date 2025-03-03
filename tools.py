import enum
import os
from pydantic import BaseModel
from datetime import datetime

from agent_choc import *
from agent_preference import *
from agent_souvenir import *
from agent_diagnostic import *



list_tool = ["detecte_choc", "detecte_preference", "detecte_souvenir","detecte_maladie"]
ToolEnum = enum.Enum("ToolEnum",
                             { item : item for item in list_tool})
from typing import List
class ToolName(BaseModel):
    tools: List[ToolEnum]