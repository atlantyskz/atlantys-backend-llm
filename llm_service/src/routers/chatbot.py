from fastapi import APIRouter, Depends
from  src.services.llm import LLMService,get_service as get_llm_service
from  src.prompts.tg_prompt import get_chatbot_system_prompt as tg_bot_system_prompt
from  src.prompts.chatbot_system_prompt import get_chatbot_system_prompt as chatbot_system_prompt
from  src.prompts.chat_history_review_prompt import get_summarizer_system_prompt
from  src.schemas.chatbot import ChatbotRequestDTO,ChatHistoryReviewRequestDTO,ChatbotResponseDTO,SummaryChatResponse
from  src.core.logger import get_logger

chatbot_router = APIRouter(prefix="/chatbot",tags=["Chatbot"])
logger = get_logger("chatbot_router")

@chatbot_router.get("/")
async def get_chatbot():
    return {"message": "Hello, World!"}


@chatbot_router.post("/generate-chat-response")
async def generate_chat_response(data:dict, llm_service: LLMService = Depends(get_llm_service)):
    logger.info(f"Received chatbot request: {data}")
    system_prompt = await chatbot_system_prompt()
    logger.info("Generating chatbot response...")
    response = await llm_service.generate_response(data,system_prompt)
    logger.info(f"Chatbot response: {response}")
    return response


@chatbot_router.post('/generate-tg-chat-response')
async def generate_tg_chat_response(data:dict,llm_service:LLMService = Depends(get_llm_service)):
    logger.info(f"Received chatbot request: {data}")
    system_prompt = await tg_bot_system_prompt()
    logger.info("Generating chatbot response...")
    response = await llm_service.generate_response(data,system_prompt,ChatbotResponseDTO)
    logger.info(f"Chatbot response: {response}")
    return response


@chatbot_router.post('/chat-history-review')
async def chat_history_review(data: ChatHistoryReviewRequestDTO, llm_service: LLMService = Depends(get_llm_service)):
    logger.info(f"Received chat history review request: {data.model_dump()}")
    system_prompt = await get_summarizer_system_prompt()
    logger.info("Generating chat history review response...")
    response = await llm_service.generate_response(data.model_dump(),system_prompt,SummaryChatResponse)
    logger.info(f"Chat history review response: {response}")
    return response