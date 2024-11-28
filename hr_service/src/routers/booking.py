from fastapi import APIRouter
from src.schemas.booking import Event
from src.services.booking import CalendarManager
booking_router = APIRouter(prefix='/api')

@booking_router.post('/create-event')
async def create_event(event_data: Event):
    manager = CalendarManager()

    event_dict = event_data.model_dump()

    event_dict['start']['dateTime'] = event_data.start.dateTime.isoformat()
    event_dict['end']['dateTime'] = event_data.end.dateTime.isoformat()

    event_link = manager.create_event(event_dict)
    response = {
        "success":True,
        "data":{
            'message':"Event successfully created",
            'event_link':event_link
        }
    }
    return response


@booking_router.get('/get-events')
async def get_events():
    manager = CalendarManager()
    return manager.get_events()


@booking_router.get('/get-event-by-id/{event_id}')
async def get_event_by_id(event_id:str):
    manager = CalendarManager()
    return manager.get_event(event_id=event_id)