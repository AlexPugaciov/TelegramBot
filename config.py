
from dotenv import load_dotenv
import os

load_dotenv('.env')
TOKEN = os.getenv('TOKEN')
REDIS_PASS = os.getenv('REDIS')
HOST = os.getenv('REDIS_HOST')
WEATHER_API = os.getenv('WEATHER_API')