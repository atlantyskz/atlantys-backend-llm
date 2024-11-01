import logging
import os
import json
from fastapi import HTTPException
from openai import AsyncOpenAI


logger = logging.getLogger(__name__)

class LLMService():
    def __init__(self):
        self.openai = AsyncOpenAI(api_key='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',base_url='https://openrouter.ai/api/v1')

    async def generate_response(self, message: str, system_prompt: str):
        try:
            response = await self.openai.chat.completions.create(
                model='openai/chatgpt-4o-latest',
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ]
            )
            full_response = response.choices[0].message.content
            logger.info(f"Generated response: {full_response}")

            llm_response = response.choices[0].message.content
            logger.info(f"Received parsed JSON response: {llm_response}")
            return json.loads(llm_response)
        except json.JSONDecodeError:
            logger.error("Failed to parse response as JSON. Returning raw content.")
            return {"response": llm_response, "error": "Response is not in JSON format."}
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise HTTPException(status_code=500, detail="An unexpected error occurred while processing the AI response.")


async def get_service():
    return LLMService()