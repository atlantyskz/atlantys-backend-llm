import datetime
from typing import List
from beanie import Document

class Message(Document):
    role: str
    content: str
    timestamp: datetime.datetime 
    class Settings:
        name = "messages"

class ChatDialogueHistory(Document):
    session_id: str
    messages: List[Message] = []
    created_at: datetime.datetime = datetime.datetime.now()
    updated_at: datetime.datetime = datetime.datetime.now()

    class Settings:
        name = "chatbot_dialogue_history"

    async def add_message(self, sender, message):
        new_message = {
            "role": sender,
            "content": message,
            "timestamp": datetime.datetime.now()
        }
        self.messages.append(new_message)
        self.updated_at = datetime.datetime.now()
        await self.save()  

