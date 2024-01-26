from motor.motor_asyncio import AsyncIOMotorClient
from api.config import mongo_db_settings

DATABASE_URL = mongo_db_settings.MONGODB_URL
DATABASE_NAME = mongo_db_settings.MONGODB_NAME

class Database:
    client: AsyncIOMotorClient = None

db = Database()

async def get_database():
    if db.client is None:
        db.client = AsyncIOMotorClient(DATABASE_URL)
    return db.client[DATABASE_NAME]


async def close_database_connection():
    if db.client is not None:
        db.client.close()


async def check_db_connection():
    try:
        client = AsyncIOMotorClient(DATABASE_URL)
        await client.admin.command("ping")

        # Get the list of available collections in the database
        database = client[DATABASE_NAME]
        collection_names = await database.list_collection_names()

        # Log the available collections
        print("Connected to the database.")
        print("Available collections:")
        for collection_name in collection_names:
            print(collection_name)

        return True
    except Exception as e:
        logging.error(f"Error connecting to the database: {e}")
        return False
