from pydantic import BaseModel
from typing import List
import datetime

class MessageShortView(BaseModel):
    sender: str
    message: str

class ChatSummaryView(BaseModel):
    session_id: str
    messages: List[MessageShortView]

