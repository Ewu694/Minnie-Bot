import asyncio
import math
from datetime import datetime
from typing import Final
import os 
from dotenv import load_dotenv
import discord 
from discord import Intents, Message, app_commands
from discord.ext import commands
import task

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
    await interaction.response.send_message('Meowdy ᓚ₍ ^. .^₎୨୧')

@client.tree.command(name='add_tasks', description='Add Tasks that you need to do!', guild=GUILD_ID)
async def add_tasks(interaction: discord.Interaction, item: str, type: int = 0) -> None:
    new_task = task.Task(item, interaction.user.display_name, type)
    if not client.task_list:
        client.task_list[1] = new_task
    else:
        client.task_list[len(client.task_list) + 1] = new_task
    await interaction.response.send_message(f'Added Task: {new_task.description} |──ᓚ₍ ^. .^₎୨୧──| ID: {len(client.task_list)} \nJust for you {interaction.user.display_name} ᓚ₍ ^. .^₎୨୧')

@client.tree.command(name='show_tasks', description='Show all items in the tasklist', guild=GUILD_ID)
async def show_tasks(interaction: discord.Interaction) -> None:
    if not client.task_list:
        await interaction.response.send_message('There are currently no tasks to be done, add some meowster ᓚ₍ ^. .^₎୨୧')
    else:
        tasks = '\n'.join(f'{key}: {value.description} |──ᓚ₍ ^. .^₎୨୧──| Task Type: {value.type} |──ᓚ₍ ^. .^₎୨୧──| Created by: {value.author}' for key, value in client.task_list.items())
        show_tasks_embed = discord.Embed(title = 'Task List', description = (f'\n{tasks}'), timestamp = datetime.now())
        await interaction.response.send_message(embed = show_tasks_embed)

@client.tree.command(name='remove_task', description='Remove a task from the tasklist', guild=GUILD_ID)
async def remove_task(interaction: discord.Interaction, task_id: int) -> None:
    if not client.task_list:
        await interaction.response.send_message('There are currently no tasks to be done! Add some meowster! ᓚ₍ ^. .^₎୨୧')
    if task_id not in client.task_list:
        await interaction.response.send_message("Task not found! Properly check the task ID using '/show_tasks' and try again :3!")
    else:
        del client.task_list[task_id]
        await interaction.response.send_message(f'Removed task with ID: {task_id} from the tasklist ᓚ₍ ^. .^₎୨୧')

@client.tree.command(name='clear_tasks', description='Clear all tasks from the tasklist', guild=GUILD_ID)
async def clear_tasks(interaction: discord.Interaction) -> None:
    if not client.task_list:
        await interaction.response.send_message('No tasks to clear ᓚ₍ ^. .^₎୨୧')
    else:
        client.task_list.clear()
        await interaction.response.send_message('Cleared all tasks meowster >:3!')

@client.tree.command(name='change_task_type', description='Change the type of a task', guild=GUILD_ID)
async def change_task_type(interaction: discord.Interaction, task_id: int, task_type: int) -> None:
    if not client.task_list:
        await interaction.response.send_message('No tasks to change! Add some meowster ᓚ₍ ^. .^₎୨୧')
    if task_id not in client.task_list:
        await interaction.response.send_message("Task not found! Properly check the task ID using '/show_tasks' and try again :3!")
    else:
        client.task_list[task_id].set_type(task_type)
        await interaction.response.send_message(f'Changed task type to {task_type} for task with ID: {task_id} ᓚ₍ ^. .^₎୨୧')

@client.tree.command(name='vote', description='Vote for whichever option you like!', guild=GUILD_ID)
async def vote(interaction: discord.Interaction, option: str, first_option: str, second_option: str) -> None:
    embed = discord.Embed(title = f'Vote for: {option}!', description = f'1️⃣ for {first_option}\n2️⃣ for {second_option}\n\nVoting ends in 10 minutes!', timestamp = datetime.now())
    await interaction.response.send_message(content = '@everyone', embed = embed, allowed_mentions=discord.AllowedMentions(everyone = True))
    message = await interaction.original_response()
    await message.add_reaction('1️⃣')
    await message.add_reaction('2️⃣')
    await asyncio.sleep(600)
    
    updated_message = await interaction.channel.fetch_message(message.id)
    yes_choice = discord.utils.get(updated_message.reactions, emoji = '1️⃣')
    no_choice = discord.utils.get(updated_message.reactions, emoji = '2️⃣')
    
    yes_choice = yes_choice.count - 1
    no_choice = no_choice.count - 1
    print(yes_choice, no_choice)
    result = 'Tie'
    if yes_choice> no_choice:
        result = first_option
    elif no_choice > yes_choice:
        result = second_option
    result_embed = discord.Embed(title = 'Vote Re sult', description = f'The result of the vote is: {result}', color = discord.Color.green(), timestamp = datetime.now())
    await interaction.followup.send(content = '@everyone', embed = result_embed, allowed_mentions = discord.AllowedMentions(everyone = True))

@client.tree.command(name='splitbill', description='Split the bill among friends!', guild=GUILD_ID)
async def split_bill(interaction: discord.Interaction, total: float, person_to_pay: discord.User, user1: discord.User, user2: discord.User, user3: discord.User = None, user4: discord.User = None, user5: discord.User = None, user6: discord.User = None, user7: discord.User = None, user8: discord.User = None, user9: discord.User = None, user10: discord.User = None) -> None:
    users = [user for user in [user1, user2, user3, user4, user5, user6, user7, user8, user9, user10] if user is not None]
    number_of_people = len(users)
    
    amount_per_person = math.ceil((total / number_of_people) * 100) / 100
    user_mentions = ', '.join(user.mention for user in users)
    embed = discord.Embed(title = 'Bill Splitting', description = f'Each person should pay: ```diff\n+ ${amount_per_person:.2f}\n```', timestamp = datetime.now())
    await interaction.response.send_message(content = f'Hey {user_mentions} pay {person_to_pay.mention} or else 😾', embed = embed)

client.run(DISCORD_TOKEN)



