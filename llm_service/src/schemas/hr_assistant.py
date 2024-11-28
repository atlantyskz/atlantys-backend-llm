from pydantic import BaseModel

class HRAssistantDTO(BaseModel):
    vacancy_requirements: str
    candidate_resume: str
