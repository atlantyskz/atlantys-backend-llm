import datetime
from fastapi import HTTPException
import httpx
from  src.core.logger import get_logger
from  src.core.settings import settings
from  src.models.chat import ChatDialogueHistory, Message
from  src.schemas.chat import ChatSummaryView


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

    async def get_chat_history(self, session_id: str):
        chat_history = await ChatDialogueHistory.find_one(ChatDialogueHistory.session_id == session_id,projection_model=ChatSummaryView)
        print(chat_history)
        return chat_history
        
    async def summarize_chat_history(self, session_id: str):
        chat_history = await self.get_chat_history(session_id)
        if not chat_history:
            raise HTTPException(status_code=404, detail="Chat history not found.")
        async with httpx.AsyncClient() as client:
            try:
                self.logger.info("Generating chat history review response...")
                data = {
                    "history_context": [
                        chat_history.model_dump()
                    ]
                }
                response = await client.post(f"http://llm_service:8001/chatbot/chat-history-review", json=data)
                response.raise_for_status()
                self.logger.info("Response generated successfully.")
                return response.json()
            except httpx.HTTPStatusError as exc:
                self.logger.info(f"HTTP error occurred: {exc}")
                raise
            except Exception as exc:
                self.logger.info(f"An error occurred: {str(exc)}")
                raise


async def get_service():
    return AiChatService()