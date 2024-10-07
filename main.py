from typing import Final
import os 
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

# Load our token from .env
load_dotenv()
DISCORD_TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Bot Setup
intents: Intents = Intents.default()
intents.message_content = True
# Client Setup for bot 
client: Client = Client(intents = intents)