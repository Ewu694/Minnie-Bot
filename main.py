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
client: Client = Client(intents = intents)

# Message Functionality
async def sendMessage(message: Message, user_message: str) -> None:
    if not user_message:
        print('Message is empty -> Intents were not enabled')
        return
    if is_private := user_message[0] == '?': # ? indicates this is a private message, so this usermessage to be sent is sliced from 1 onwards and stored in is_private and sent to the user after the response is generated
        user_message = user_message[1:]
    
    try:
        # if message is private, send the response to the user, else send the response to the channel
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response) 
    except Exception as error:
        print(f'Error: {error}')

# Bot Handling
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')