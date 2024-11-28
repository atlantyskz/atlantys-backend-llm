from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from src.core.logger import get_logger  

class Store:

    def __init__(self):
        from src.core.db import MongoDbAccessor
        self.db = MongoDbAccessor()
        self.logger = get_logger("store")

    async def connect(self)->None:
        await self.db.connect_to_mongoDB()
        self.logger.info("Connected to Store")

    async def disconnect(self)->None:
        await self.db.disconnect_from_mongoDB() 
        self.logger.info("Disconnected from Store")

_store:Store|None = None


def get_store() -> Store:
    return _store


async def connect_to_store() -> Store:
    global _store

    if not _store:
        _store = Store()
        await _store.connect()

    return _store


async def disconnect_from_store() -> None:
    global _store

    if _store:
        await _store.disconnect()
        _store = None



@asynccontextmanager
async def store_lifespan() -> AsyncGenerator[Store, None]:
    await connect_to_store()
    try:
        yield get_store()
    finally:
        await disconnect_from_store()


@asynccontextmanager
async def lifespan(*_: FastAPI) -> AsyncGenerator[None, None]:
    async with store_lifespan():
        yield