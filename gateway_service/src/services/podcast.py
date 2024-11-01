import logging
import httpx

class PodcastService:

    async def generate_podcast(self, topic: str, url: str):
        async with httpx.AsyncClient(timeout=10) as client:
            try:
                logging.info("Sending request to generate podcast...")
                response = await client.post("http://llm_service:8001/generate-podcast", json={"topic": topic, "url": url})
                response.raise_for_status()
                logging.info("Podcast generated successfully.")
                return response.json()
            except httpx.HTTPStatusError as exc:
                logging.error(f"HTTP error occurred: {exc}")
                raise
            except Exception as exc:
                logging.error(f"An error occurred: {exc}")
                raise        
async def get_service():
    return PodcastService()