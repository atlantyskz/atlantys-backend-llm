from fastapi import APIRouter,Depends
from fastapi.responses import FileResponse
from  src.services.audio_generate import AudioGenerateService,get_service as get_audio_generate_service
from  src.services.podcast import PodcastService,get_service as get_podcast_service
from  src.schemas.podcast import PodcastRequestDTO

gateway_router = APIRouter()

@gateway_router.get("/health-check")
async def health_check():
    return {"message": "Hello, World from Gateway Service!"}

@gateway_router.post("/generate-audio-podcast")
async def generate_audio_podcast(data:PodcastRequestDTO,
                                audio_service: AudioGenerateService = Depends(get_audio_generate_service),
                                podcast_service: PodcastService = Depends(get_podcast_service)
                                ):
    dialogue_json = await podcast_service.generate_podcast(data.topic,data.url)
    audio_response = await audio_service.process_audio(dialogue_json)
    return FileResponse(audio_response, media_type="audio/mpeg", filename="podcast.mp3")    
