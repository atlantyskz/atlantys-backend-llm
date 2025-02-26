import pprint
from typing import Any
from dotenv import load_dotenv
from openai import AsyncOpenAI
import os
import json
from fastapi import HTTPException
from pydantic import BaseModel
from logging import getLogger


class LLMService:
    def __init__(self):
        load_dotenv()
        self.openai = AsyncOpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url=os.getenv("OPENROUTER_BASE_URL")
        )
        print(os.getenv("OPENROUTER_API_KEY"), os.getenv("OPENROUTER_BASE_URL"))
        self.logger = getLogger("llm_service")


            
    async def generate_response(self, data: dict, system_prompt: str):
        try:
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(data.get('messages'))
            response = await self.openai.chat.completions.create(
                model='gpt-4o-mini-2024-07-18',
                messages=messages
            )

            llm_response = response.choices[0].message.content
            tokens_spent = response.usage.total_tokens

            if isinstance(llm_response, bytes):
                llm_response = llm_response.decode('utf-8')

            parsed_response = json.loads(llm_response)
            return {
                'tokens_spent': tokens_spent,
                'llm_response': parsed_response
            }
        except json.JSONDecodeError:
            self.logger.error("Failed to parse response as JSON. Returning raw content.")
            return {"response": llm_response, "error": "Response is not in JSON format."}
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            raise HTTPException(status_code=500, detail="An unexpected error occurred while processing the AI response.")

async def get_service():
    return LLMService()