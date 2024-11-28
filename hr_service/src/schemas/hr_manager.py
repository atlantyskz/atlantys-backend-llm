from pydantic import BaseModel

class AnalyzeResumeDTO(BaseModel):
    vacancy_requirements: str
    candidate_resume:str
