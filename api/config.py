from pathlib import Path

from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv
import os

env_file = os.getenv("ENV_FILE", ".env")

basepath = Path()
basedir = str(basepath.cwd())
envars = basepath.cwd() / env_file

load_dotenv(envars)

@lru_cache
class ClickupSettings(BaseSettings):
    CLICKUP_API_KEY: str
    CLICKUP_TEAM_ID: str
    CLICKUP_WEBHOOK_ENDPOINT: str

@lru_cache()
class MongoDBSettings(BaseSettings):
    MONGODB_URL: str
    MONGODB_NAME: str

clickup_settings = ClickupSettings()
mongo_db_settings = MongoDBSettings()
