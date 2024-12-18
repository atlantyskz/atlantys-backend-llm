from typing import List, Optional
from pydantic import BaseModel

class HRAssistantDTO(BaseModel):
    vacancy_text: str
    cv_text: str

class Text(BaseModel):
    user_message:str

class CandidateInfo(BaseModel):
    fullname: str
    gender: str
    age: int
    birth_date: str
    contacts: dict
    location: str
    languages: List[str]


class JobPreferences(BaseModel):
    desired_position: str
    employment_type: str
    work_schedule: str
    desired_salary: Optional[str] = None


class ExperienceDetails(BaseModel):
    duration: str
    company_name: str
    role: str


class Education(BaseModel):
    degrees: List[str]


class Analysis(BaseModel):
    advantages: List[str]
    disadvantages: List[str]
    overall_comment: str


class HRCandidateAnalysis(BaseModel):
    candidate_info: CandidateInfo
    job_preferences: JobPreferences
    experience: List[ExperienceDetails]
    education: Education
    skills: List[str]
    analysis: Analysis


class JobVacancy(BaseModel):
    job_title: str
    specialization: str
    salary_range: Optional[str] = None
    company_name: str
    experience_required: str
    work_format: str
    work_schedule: str
    responsibilities: list[str]
    requirements: list[str]
    conditions: list[str]
    skills: list[str]
    address: str
    contacts: Optional[str] = None
    location: str