import json
import re
from typing import Optional
from fastapi import APIRouter, Body,Depends, File, Form, HTTPException, UploadFile
from  src.services.llm import LLMService,get_service as get_llm_service
from  src.services.extractor import UrlExtractorService,get_service as get_url_extractor_service
from  src.schemas.hr_assistant import *
from src.prompts.hr_assistant_prompt import get_hr_assistant_system_prompt
from src.prompts.vacancy_maker_prompt import get_vacancy_maker_system_prompt


hr_assistant_router = APIRouter(prefix="/hr")


@hr_assistant_router.post("/analyze_cv_by_vacancy")
async def analyze_cv_by_vacancy(data:HRAssistantDTO, llm_service:LLMService = Depends(get_llm_service)):
    system_prompt = await get_hr_assistant_system_prompt()
    res = await llm_service.generate_response(data.model_dump(),system_prompt)
    return res 

@hr_assistant_router.post("/generate_vacancy",)
async def create_vacancy(
    user_data:VacancyMaker = Body(...),
    llm_service: LLMService = Depends(get_llm_service)
):
    system_prompt = await get_vacancy_maker_system_prompt()
    response = await llm_service.generate_response(user_data, system_prompt, )
    return response
