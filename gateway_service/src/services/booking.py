from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build

class IAuthManager(ABC):
    @abstractmethod
    def get_service(self):
        pass


class GoogleAuthManager(IAuthManager):
    def __init__(self, key_file: str, user_email: str, scopes: List[str]):
        credentials = service_account.Credentials.from_service_account_file(key_file, scopes=scopes)
        self.delegated_credentials = credentials.with_subject(user_email)

    def get_service(self):
        return build('calendar', 'v3', credentials=self.delegated_credentials)


class IEventCreator(ABC):
    @abstractmethod
    def create_event(self, calendar_id: str, event_data: Dict) -> str:
        pass


class IEventReader(ABC):
    @abstractmethod
    def get_events(self, calendar_id: str) -> List[Dict]:
        pass

    @abstractmethod
    def get_event(self, calendar_id: str, event_id: str) -> Optional[Dict]:
        pass


class CalendarManager(IEventCreator, IEventReader):
    def __init__(self, auth_manager: IAuthManager):
        self.service = auth_manager.get_service()

    def create_event(self, calendar_id: str, event_data: Dict) -> str:
        event = self.service.events().insert(calendarId=calendar_id, body=event_data).execute()
        return event.get("htmlLink")

    def get_events(self, calendar_id: str) -> List[Dict]:
        events = self.service.events().list(calendarId=calendar_id).execute()
        return events.get("items", [])

    def get_event(self, calendar_id: str, event_id: str) -> Optional[Dict]:
        event = self.service.events().get(calendarId=calendar_id, eventId=event_id).execute()
        return event
