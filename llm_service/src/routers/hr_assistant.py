import json
import re
from fastapi import APIRouter,Depends
from  src.services.llm import LLMService,get_service as get_llm_service
from  src.services.extractor import UrlExtractorService,get_service as get_url_extractor_service
from  src.schemas.hr_assistant import HRAssistantDTO
from src.prompts.hr_assistant_prompt import get_hr_assistant_system_prompt


hr_assistant_router = APIRouter()

def prepare_for_json(text: str) -> str:
    # Заменяем символы новой строки, возврата каретки и табуляции на их экранированные версии
    text = text.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
    # Также можно использовать json.dumps, чтобы экранировать любые другие символы
    return json.dumps(text)

# Ваш эндпоинт
@hr_assistant_router.post('/analyze_cv')
async def analyze_cv(data: HRAssistantDTO, llm_service: LLMService = Depends(LLMService)):
    try:
        system_prompt = await get_hr_assistant_system_prompt()

        # Применяем предобработку к текстам
        candidate_resume = prepare_for_json(data.candidate_resume)

        # Теперь возвращаем отформатированные данные
        return {
            "vacancy_requirements": data.vacancy_requirements,
            "candidate_resume": candidate_resume
        }

    except Exception as e:
        return {"error": str(e)}