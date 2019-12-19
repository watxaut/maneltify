import os

from dotenv import load_dotenv

load_dotenv()

# gimp
JSON_FACES_PATH = os.getenv("JSON_FACES_PATH", "None")
JSON_BACKGROUNDS_PATH = os.getenv("JSON_BACKGROUNDS_PATH", "None")

# telegram
TOKEN = os.getenv("TELEGRAM_TOKEN", None)
