import os
import json
from fastapi import HTTPException
from openai import AsyncOpenAI
from  src.core.logger import get_logger
from dotenv import load_dotenv


class LLMService():
    def __init__(self):
        load_dotenv()
        self.openai = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"),base_url=os.getenv("OPENROUTER_BASE_URL"),)
        self.logger = get_logger("llm_service") 
        print(os.getenv("OPENAI_API_KEY"))

    async def generate_response(self, message: dict, system_prompt: str):
        try:
            response = await self.openai.chat.completions.create(
                model='openai/gpt-4o-mini-2024-07-18',
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": f"{message}"
                    }
                ]
            )
            full_response = response.choices[0].message.content
            self.logger.info(f"Generated response: {full_response}")

            llm_response = response.choices[0].message.content
            self.logger.info(f"Received parsed JSON response: {llm_response}")
            return json.loads(llm_response)
        except json.JSONDecodeError:
            self.logger.error("Failed to parse response as JSON. Returning raw content.")
            return {"response": llm_response, "error": "Response is not in JSON format."}
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            raise HTTPException(status_code=500, detail="An unexpected error occurred while processing the AI response.")


        

async def get_service():
    return LLMService()