from typing import Final
import os 
from dotenv import load_dotenv
import discord 
from discord import Intents, Client, Message
class Client(discord.client):
    async def on_bot_ready() -> None:
        print(f'{client.user} is now running!')
    
    async def on_message(self, message: Message):
        if message.author == self.user:
            return
        
        if message.content.startswith('hello'):
            await message.channel.send(f'Meowdy {message.author}!')

# Load our token from .env
load_dotenv()
DISCORD_TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Bot Setup
intents: Intents = discord.Intents.default()
intents.message_content = True
client: Client = Client(intents = intents)
