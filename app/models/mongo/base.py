from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel
from bson import ObjectId

class BaseMongoModel(BaseModel):
    id: str | None = None

    @classmethod
    async def get(cls, db: AsyncIOMotorDatabase, collection: str, query: dict):
        return await db[collection].find_one(query)

    @classmethod
    async def get_all(cls, db: AsyncIOMotorDatabase, collection: str, query: dict = {}):
        return await db[collection].find(query).to_list(1000)

    @classmethod
    async def create(cls, db: AsyncIOMotorDatabase, collection: str, data: dict):
        result = await db[collection].insert_one(data)
        return str(result.inserted_id)

    @classmethod
    async def update(cls, db: AsyncIOMotorDatabase, collection: str, query: dict, data: dict):
        await db[collection].update_one(query, {"$set": data})

    @classmethod
    async def delete(cls, db: AsyncIOMotorDatabase, collection: str, query: dict):
        await db[collection].delete_one(query)
