import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from abc import ABC, abstractmethod
from dotenv import load_dotenv

class IEventCreator(ABC):
    @abstractmethod
    async def create_event(self, event_data: dict):
        pass

class IEventReader(ABC):
    @abstractmethod
    def get_event(self, event_id: str):
        pass

    @abstractmethod
    def get_events(self):
        pass

class CalendarManager(IEventReader, IEventCreator):
    load_dotenv()

    GOOGLE_KEY_FILE = os.getenv("GOOGLE_KEY_FILE")
    GOOGLE_USER_EMAIL = os.getenv("GOOGLE_USER_EMAIL")
    SCOPES = [os.getenv('GOOGLE_SCOPES_CALENDAR'),os.getenv('GOOGLE_SCOPES_CALENDAR_EVENTS')]
    calendarId = os.getenv('GOOGLE_CALENDAR_ID')

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(self.GOOGLE_KEY_FILE, scopes=self.SCOPES)
        delegated_credentials = credentials.with_subject(self.GOOGLE_USER_EMAIL)
        self.service = build('calendar', 'v3', credentials=delegated_credentials)

    def create_event(self, event_data: dict):
        attendees = [{"email": email} for email in event_data.get('attendees', [])]
        event_data['attendees'] = attendees

        event_data['reminders'] = {
            "useDefault": False,  
            "overrides": [
                {"method": "email", "minutes": 1440},  
                {"method": "email", "minutes": 60},    
            ]
        }

        event = self.service.events().insert(
            calendarId=self.calendarId,
            body=event_data,
            sendNotifications=True  
        ).execute()

        return event.get("htmlLink")

    def get_events(self):
        events = self.service.events().list(calendarId=self.calendarId).execute()
        return events.get("items", [])

    def get_event(self, event_id: str):
        event = self.service.events().get(calendarId=self.calendarId, eventId=event_id).execute()
        return event


