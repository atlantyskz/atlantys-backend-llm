from fastapi import APIRouter, Depends
from  src.services.llm import LLMService,get_service as get_llm_service
from  src.prompts.chatbot_system_prompt import get_chatbot_system_prompt
from  src.schemas.chatbot import ChatbotRequestDTO
from  src.core.logger import get_logger

chatbot_router = APIRouter(prefix="/chatbot",tags=["Chatbot"])
logger = get_logger("chatbot_router")

@chatbot_router.get("/")
async def get_chatbot():
    return {"message": "Hello, World!"}


@chatbot_router.post("/generate-chat-response")
async def generate_chat_response(data:ChatbotRequestDTO, llm_service: LLMService = Depends(get_llm_service)):
    logger.info(f"Received chatbot request: {data.model_dump()}")
    system_prompt = await get_chatbot_system_prompt()
    logger.info("Generating chatbot response...")
    response = await llm_service.generate_response(data.model_dump(),system_prompt)
    logger.info(f"Chatbot response: {response}")
    return response

