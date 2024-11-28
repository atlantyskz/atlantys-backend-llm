from fastapi import APIRouter
from src.schemas.hr_manager import AnalyzeResumeDTO

hr_manager_router = APIRouter('/api')

@hr_manager_router.post('/analyze_resume_by_vacancy_requirements')
async def analyze_resume_by_vacancy_requirements(data:AnalyzeResumeDTO):
    ...