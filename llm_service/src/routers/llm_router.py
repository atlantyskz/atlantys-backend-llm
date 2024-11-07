from fastapi import APIRouter,Depends
from  src.services.llm import LLMService,get_service as get_llm_service
from  src.services.extractor import UrlExtractorService,get_service as get_url_extractor_service
from  src.schemas.podcast import PodcastRequestDTO
from  src.prompts.demo_podcast_system_prompt import get_demo_podcast_system_prompt

llm_router = APIRouter(prefix="/podcast",tags=["Podcast"])

@llm_router.get("/")
async def get_llm():
    return {"message": "Hello, World!"}

@llm_router.post("/generate-podcast")
async def generate_podcast( data:PodcastRequestDTO, 
                            llm_service: LLMService = Depends(get_llm_service),
                            url_service: UrlExtractorService = Depends(get_url_extractor_service)
                            ):
    extracted_content = await url_service.extract_content_from_url(data.url) 
    system_prompt = await get_demo_podcast_system_prompt(data.topic,extracted_content)
    response =  await llm_service.generate_response(data.topic,system_prompt)
    return response
