from pydantic import BaseModel
from typing import List


class ChatbotRequestDTO(BaseModel):
    message: str
    history_context: List[dict]

    class Config:
        from_attributes = True