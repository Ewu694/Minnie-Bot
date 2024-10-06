from typing import Final
import os 
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

#STEP 0: Load our token from .env
load_dotenv()
DISCORD_TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
print(DISCORD_TOKEN)