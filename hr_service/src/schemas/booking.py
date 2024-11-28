from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr


class EventDateTime(BaseModel):
    dateTime: datetime
    timeZone: str = "Asia/Almaty"  


    class Config:
        from_attributes = True

class Event(BaseModel):
    summary: str
    location: str
    description: str
    start: EventDateTime
    end: EventDateTime
    attendees: List[EmailStr]  


    class Config:
        from_attributes = True
