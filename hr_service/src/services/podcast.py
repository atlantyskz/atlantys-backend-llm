import httpx
from  src.core.logger import get_logger
from  src.core.settings import settings


class PodcastService:

    def __init__(self):
        self.logger = get_logger("podcast_service")

    async def generate_podcast(self, topic: str, url: str):
        async with httpx.AsyncClient(timeout=10) as client:
            try:
                self.logger.info("Generating podcast...")
                response = await client.post(f"http://llm_service:8001/podcast/generate-podcast", json={"topic": topic, "url": url})
                response.raise_for_status()
                self.logger.info("Podcast generated successfully.")
                return response.json()
            except httpx.HTTPStatusError as exc:
                self.logger.info(f"HTTP error occurred: {exc}")
                raise
            except Exception as exc:
                self.logger.info(f"An error occurred: {exc}")
                raise   



async def get_service():
    return PodcastService()