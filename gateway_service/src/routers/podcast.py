from fastapi import APIRouter,Depends
from fastapi.responses import FileResponse
from services.audio_generate import AudioGenerateService,get_service as get_audio_generate_service
from services.podcast import PodcastService,get_service as get_podcast_service
from schemas.podcast import PodcastRequestDTO
from prompts.demo_podcast_system_prompt import get_demo_podcast_system_prompt

gateway_router = APIRouter()

@gateway_router.get("/")
async def get_llm():
    return {"message": "Hello, World!"}

@gateway_router.post("/generate-audio-podcast")
async def generate_audio_podcast(data:PodcastRequestDTO,
                                audio_service: AudioGenerateService = Depends(get_audio_generate_service),
                                podcast_service: PodcastService = Depends(get_podcast_service)
                                ):
    dialogue_json = await podcast_service.generate_podcast(data.topic,data.url)
    audio_response = await audio_service.process_audio(dialogue_json)
    return FileResponse(audio_response, media_type="audio/mpeg", filename="podcast.mp3")    
