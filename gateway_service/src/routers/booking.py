from fastapi import APIRouter

booking_router = APIRouter()

@booking_router.post('/create-event')
async def create_event():
    
    return {"message": "Event created successfully."}
