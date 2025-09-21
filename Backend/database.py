import os
from motor.motor_asyncio import AsyncIOMotorClient


# MONGO_URL = "mongodb://localhost:27017"
# MONGO_URL = "mongodb+srv://premsingh314work_db_user:YzmGJozMAiiNi4aM@soulbloom.6mheqxb.mongodb.net/?retryWrites=true&w=majority&appName=Soulbloom"
MONGO_URL = os.environ.get("MONGO_URL")
DB_NAME = "Soulbloom"

client: AsyncIOMotorClient = AsyncIOMotorClient(MONGO_URL)

db = client[DB_NAME]
chats = db["user_chats"]