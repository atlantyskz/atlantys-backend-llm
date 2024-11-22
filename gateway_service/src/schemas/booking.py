from pydantic import BaseModel

class Event(BaseModel):
    summary: str
    location: str
    description: str
    start: str  # Формат '2024-11-15T09:00:00-07:00'
    end: str    # Формат '2024-11-15T10:00:00-07:00'
    timeZone: str = "Asia/Almaty"