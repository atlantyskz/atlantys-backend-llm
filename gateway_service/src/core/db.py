import os
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from src.models.chat import ChatDialogueHistory,Message
from src.core.logger import get_logger
from dotenv  import load_dotenv


class MongoDbAccessor:

    def __init__(self,):
        load_dotenv()
        uri = os.getenv("MONGO_DB_URI")
        print(uri)
        self.client = AsyncIOMotorClient(uri)
        self.logger = get_logger("mongodb")
    
    async def connect_to_mongoDB(self):
        await init_beanie(database=self.client.atlantys, document_models=[ChatDialogueHistory,Message])     
        uri = os.getenv("MONGO_DB_URI")

        self.logger.info(f"Connected to MongoDB - {uri}")


    async def disconnect_from_mongoDB(self,):
        self.client.close()