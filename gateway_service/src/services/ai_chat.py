import datetime
import httpx
from  src.core.logger import get_logger
from  src.core.settings import settings
from  src.models.chat import ChatDialogueHistory, Message


class AiChatService:

    def __init__(self):
        self.logger = get_logger("ai_chat_service")

    async def handle_ai_chat_response(self, message: dict):
        async with httpx.AsyncClient() as client:
            try:
                self.logger.info("Generating chatbot response...")
                response = await client.post(f"http://llm_service:8001/chatbot/generate-chat-response", json=message)
                response.raise_for_status()
                self.logger.info("Response generated successfully.")
                return response.json()
            except httpx.HTTPStatusError as exc:
                self.logger.info(f"HTTP error occurred: {exc}")
                raise
            except Exception as exc:
                self.logger.info(f"An error occurred: {str(exc)}")
                raise   

    async def save_message(self, session_id: str, sender: str, message: str):
        chat_history = await ChatDialogueHistory.find_one(ChatDialogueHistory.session_id == session_id)
        if not chat_history:
            chat_history = ChatDialogueHistory(session_id=session_id, messages=[])
        await chat_history.add_message(sender, message)
        

async def get_service():
    return AiChatService()