import asyncio
from datetime import datetime
from typing import Final
import os 
from dotenv import load_dotenv
import discord 
from discord import Intents, Message, app_commands
from discord.ext import commands

# Load our tokens from .env
load_dotenv()
DISCORD_TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
GUILD_ID = discord.Object(id=os.getenv('DISCORD_SERVER_ID'))

class Client(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_list = {}

    async def on_ready(self):
        print(f'Meowat your service {self.user}!')
        try:
            synced = await self.tree.sync(guild=GUILD_ID)
            print(f'Synced {len(synced)} commands to server {GUILD_ID}!')
        except Exception as e:
            print(f'Failed to sync commands to server {GUILD_ID}!')
            print(f'Error: {e}')
    
    async def on_message(self, message: Message):
        if message.author == self.user:
            return
        
        if message.content.startswith('hello'):
            await message.channel.send(f'Meowdy {message.author}!')

# Bot Setup
intents: Intents = discord.Intents.default()
intents.message_content = True

client = Client(command_prefix="!", intents=intents)

@client.tree.command(name='hello', description='Say hello to the bot!', guild=GUILD_ID)
async def bot_hello(interaction: discord.Interaction) -> None:
    await interaction.response.send_message('Meowdy! :3')

@client.tree.command(name='addtasks', description='Add Tasks that you need to do!', guild=GUILD_ID)
async def add_tasks(interaction: discord.Interaction, item: str) -> None:
    if not client.task_list:
        client.task_list[1] = item
    else:
        client.task_list[len(client.task_list) + 1] = item
    await interaction.response.send_message(f'Added task: {item}')

@client.tree.command(name='showtasks', description='Show all items in the tasklist', guild=GUILD_ID)
async def show_tasks(interaction: discord.Interaction) -> None:
    if not client.task_list:
        await interaction.response.send_message('There are currently no tasks to be done!')
    else:
        tasks = '\n'.join(f'{key}: {value}' for key, value in client.task_list.items())
        await interaction.response.send_message(f'Tasks to do:\n{tasks}')

@client.tree.command(name='removetask', description='Remove a task from the tasklist', guild=GUILD_ID)
async def remove_task(interaction: discord.Interaction, task_id: int) -> None:
    if not client.task_list:
        await interaction.response.send_message('There are currently no tasks to be done!')
    if task_id not in client.task_list:
        await interaction.response.send_message('Task not found!')
    else:
        del client.task_list[task_id]
        await interaction.response.send_message(f'Removed task with ID: {task_id}')

@client.tree.command(name='cleartasks', description='Clear all tasks from the tasklist', guild=GUILD_ID)
async def clear_tasks(interaction: discord.Interaction) -> None:
    if not client.task_list:
        await interaction.response.send_message('No tasks to clear!')
    else:
        client.task_list.clear()
        await interaction.response.send_message('Cleared all tasks!')

@client.tree.command(name='vote', description='Vote for whichever option you like!', guild=GUILD_ID)
async def vote(interaction: discord.Interaction, option: str, first_option: str, second_option: str) -> None:
    embed = discord.Embed(title = f'Vote for: {option}!', description = f'1️⃣ for {first_option}\n2️⃣ for {second_option}\nVoting ends in 10 minutes!', timestamp = datetime.now())
    await interaction.response.send_message(embed = embed)
    message = await interaction.original_response()
    await message.add_reaction('1️⃣')
    await message.add_reaction('2️⃣')
    await asyncio.sleep(5)
    
    print(message)
    yes_choice = await message.reactions
    no_choice = await message.reactions
    
    result = 'Tie'
    if len(yes_choice) > len(no_choice):
        result = first_option
    elif len(no_choice) > len(yes_choice):
        result = second_option
    embed = discord.Embed(title='Vote Result', description=f'The result of the vote is: {result}')
    await interaction.response.send_message(embed=embed)

client.run(DISCORD_TOKEN)



