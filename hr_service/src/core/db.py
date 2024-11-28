import os
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from src.models.chat import ChatDialogueHistory,Message
from src.core.logger import get_logger


class MongoDbAccessor:

    def __init__(self,):
        self.client = AsyncIOMotorClient(os.getenv("MONGO_DB_URI"))
        self.logger = get_logger("mongodb")
    
    async def connect_to_mongoDB(self):
        await init_beanie(database=self.client.atlantys, document_models=[ChatDialogueHistory,Message])     
        self.logger.info(f"Connected to MongoDB - {self.client.HOST}")


    async def disconnect_from_mongoDB(self,):
        self.client.close()