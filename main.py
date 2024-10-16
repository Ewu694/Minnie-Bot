import asyncio
import math
from datetime import datetime
from typing import Final
import os 
from dotenv import load_dotenv
import discord 
from discord import Intents, Message, app_commands
from discord.ext import commands
from task import Task

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
    
    async def schedule_task_deletion(self, task_id: int, delay: int):
        await asyncio.sleep(delay)
        if task_id in self.task_list:
            task = self.task_list[task_id]
            if task.repeating_task == 1:
                if task.repeating_counter == 'inf':
                    self.loop.create_task(self.schedule_task_deletion(task_id, delay))
                    print(f'Task with ID {task_id} is repeating and will be rescheduled.')
                elif task.repeating_counter > 0:
                    task.repeating_counter -= 1
                    self.loop.create_task(self.schedule_task_deletion(task_id, delay))
                    print(f'Task with ID {task_id} is repeating and will be rescheduled.')
                else:
                    del self.task_list[task_id]
                    print(f'Task with ID {task_id} has been deleted after {delay} seconds.')
            else:
                del self.task_list[task_id]
                print(f'Task with ID {task_id} has been deleted after {delay} seconds.')
        else:
            print(f'Task was completed earlier than set time ᓚ₍ ^. .^₎୨୧')

# Bot Setup
intents: Intents = discord.Intents.default()
intents.message_content = True

client = Client(command_prefix="!", intents=intents)

@client.tree.command(name='hello', description='Say hello to the bot!', guild=GUILD_ID)
async def bot_hello(interaction: discord.Interaction) -> None:
    await interaction.response.send_message('Meowdy ᓚ₍ ^. .^₎୨୧')

@client.tree.command(name='add_task', description='Add Tasks that you need to do!', guild=GUILD_ID)
async def add_task(interaction: discord.Interaction, task_description: str, repeating_task: int = 0, task_type: int = 0) -> None:
    if task_type not in [0, 1, 2, 3, 4, 5]:
        await interaction.response.send_message('Invalid task type! Task type should be 0, 1, 2, 3, or 4! 0 for one-time, 1 for daily, 2 for weekly, 3 for monthly, and 4 for yearly. Your task type will be defaulted to 0 ᓚ₍ ^. .^₎୨୧')
        task_type = 0
    if repeating_task not in [0, 1]:
        await interaction.response.send_message('Invalid repeating task value! Repeating task should be 0 or 1! 0 for non-repeating and 1 for repeating. Your repeating task value will be defaulted to 0 ᓚ₍ ^. .^₎୨୧')
        repeating_task = 0
    if task_type == 0 and repeating_task == 1:
        task_type = 0
        repeating_task = 0 
    new_task = Task(task_description, interaction.user.display_name, repeating_task, task_type)
    task_id = max(client.task_list.keys(), default=0) + 1
    client.task_list[task_id] = new_task

    print(f'Task added: {new_task.description}, ID: {task_id}, Type: {task_type}')
    print(client.task_list if client.task_list else "Task wasn't added")

    if task_type == 1: # daily task
        delay = 24 * 60 * 60 
        delay_str = "24 hours"
    elif task_type == 2: # weekly task
        delay = 7 * 24 * 60 * 60 
        delay_str = "a week"
    elif task_type == 3: # monthly task
        delay = 30 * 24 * 60 * 60
        delay_str = "30 days"
    elif task_type == 4: # yearly task
        delay = 365 * 24 * 60 * 60 
        delay_str = "a year"
    # elif task_type == 5: # testing task
    #     delay = 10
    #     delay_str = "10 seconds"
    else: # one-time task
        delay = None
        delay_str = None


    if delay:
        client.loop.create_task(client.schedule_task_deletion(task_id, delay))

    task_embed = discord.Embed(title = "Task Added", description = f'Added Task: {new_task.description} |──ᓚ₍ ^. .^₎୨୧──| ID: {task_id} \nJust for you {interaction.user.display_name} ᓚ₍ ^. .^₎୨୧')
    if delay_str and repeating_task == 1:
        task_embed.set_footer(text=f'This is a repeating task and will be rescheduled to be deleted later ᓚ₍ ^. .^₎୨୧')
    elif delay_str and repeating_task == 0:
        task_embed.set_footer(text="This task will be deleted or rescheduled after {delay_str}  ᓚ₍ ^. .^₎୨୧")
    elif delay_str:
        task_embed.set_footer(text=f'This task will be deleted after {delay_str} ᓚ₍ ^. .^₎୨୧')
    else:
        task_embed.set_footer(text="This is a one-time task and must be deleted manually using '/remove_task' ᓚ₍ ^. .^₎୨୧")

    await interaction.response.send_message(embed = task_embed)

@client.tree.command(name='show_tasks', description='Show all items in the tasklist', guild=GUILD_ID)
async def show_tasks(interaction: discord.Interaction) -> None:
    if client.task_list:
        tasks = '\n'.join(f'{key}: {value.description} |──ᓚ₍ ^. .^₎୨୧──| Task Type: {value.type} |──ᓚ₍ ^. .^₎୨୧──| Created by: {value.author}' for key, value in client.task_list.items())
        show_tasks_embed = discord.Embed(title = 'Task List', description = (f'\n{tasks}'), timestamp = datetime.now())
        await interaction.response.send_message(embed = show_tasks_embed)
    else:
        await interaction.response.send_message('There are currently no tasks to be done, add some meowster ᓚ₍ ^. .^₎୨୧')

@client.tree.command(name='remove_task', description='Remove a task from the tasklist', guild=GUILD_ID)
async def remove_task(interaction: discord.Interaction, task_id: int) -> None:
    if not client.task_list:
        await interaction.response.send_message('There are currently no tasks to be done! Add some meowster! ᓚ₍ ^. .^₎୨୧')
        return
    if task_id not in client.task_list:
        await interaction.response.send_message("Task not found! Properly check the task ID using '/show_tasks' and try again :3!")
        return
    task = client.task_list[task_id]
    if task.repeating_task == 1:
        if task.type == 1: # daily task
            delay = 24 * 60 * 60 
            delay_str = "24 hours"
        elif task.type == 2: # weekly task
            delay = 7 * 24 * 60 * 60 
            delay_str = "a week"
        elif task.type == 3: # monthly task
            delay = 30 * 24 * 60 * 60
            delay_str = "30 days"
        elif task.type == 4: # yearly task
            delay = 365 * 24 * 60 * 60 
            delay_str = "a year"
        # elif task.type == 5: # testing task
        #     delay = 5
        #     delay_str = "5 seconds"
        else: # one-time task
            delay = None
            delay_str = None
        client.loop.create_task(client.schedule_task_deletion(task_id, delay))
        await interaction.response.send_message(f'Task with ID {task_id} is a repeating task and will be rescheduled to be deleted later ᓚ₍ ^. .^₎୨୧')
        if delay_str:
            remove_embed.set_footer(text=(f'Task will be set to expire in {delay_str}!'))
        return

    del client.task_list[task_id]
    remove_embed = discord.Embed(title = 'Task Removed', description=(f'Removed task with ID: {task_id} ᓚ₍ ^. .^₎୨୧'), timestamp = datetime.now())
    await interaction.response.send_message(embed = remove_embed)

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

@client.tree.command(name='change_task_description', description='Change the description of a task', guild=GUILD_ID)
async def change_task_description(interaction: discord.Interaction, task_id: int, description: str) -> None:
    if not client.task_list:
        await interaction.response.send_message('No tasks to change! Add some meowster ᓚ₍ ^. .^₎୨୧')
    if task_id not in client.task_list:
        await interaction.response.send_message("Task not found! Properly check the task ID using '/show_tasks' and try again :3!")
    else:
        client.task_list[task_id].set_description(description)
        await interaction.response.send_message(f'Changed task description to {description} for task with ID: {task_id} ᓚ₍ ^. .^₎୨୧')

@client.tree.command(name='change_repeating_counter', description='Change the repeating counter of a task to make it loop a certain amount of times', guild=GUILD_ID)
async def change_repeating_counter(interaction: discord.Interaction, task_id: int, repeating_counter: str) -> None:
    if not client.task_list:
        await interaction.response.send_message('No tasks to change! Add some meowster ᓚ₍ ^. .^₎୨୧')
    if task_id not in client.task_list:
        await interaction.response.send_message("Task not found! Properly check the task ID using '/show_tasks' and try again :3!")
    elif client.task_list[task_id].repeating_task == 0:
        await interaction.response.send_message("Task is not a repeating task! Change the task to a repeating task using '/change_task_type' and try again :3!")
    else:
        client.task_list[task_id].set_repeating_counter(repeating_counter)
        await interaction.response.send_message(f'Changed repeating counter to {repeating_counter} for task with ID: {task_id} ᓚ₍ ^. .^₎୨୧')

@client.tree.command(name='vote', description='Vote for whichever option you like!', guild=GUILD_ID)
async def vote(interaction: discord.Interaction, option: str, first_option: str, second_option: str, voting_duration: int) -> None:
    embed = discord.Embed(title = f'Vote for: {option}!', description = f'1️⃣ for {first_option}\n2️⃣ for {second_option}\n\nVoting ends in {voting_duration} minutes!', timestamp = datetime.now())
    await interaction.response.send_message(content = '@everyone', embed = embed, allowed_mentions=discord.AllowedMentions(everyone = True))
    message = await interaction.original_response()
    await message.add_reaction('1️⃣')
    await message.add_reaction('2️⃣')
    await asyncio.sleep(voting_duration * 60)
    
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
    result_embed = discord.Embed(title = 'Vote Result', description = f'The result of the vote is: {result}', color = discord.Color.green(), timestamp = datetime.now())
    await interaction.followup.send(content = '@everyone', embed = result_embed, allowed_mentions = discord.AllowedMentions(everyone = True))
    

@client.tree.command(name='split_bill', description='Split the bill among friends!', guild=GUILD_ID)
async def split_bill(interaction: discord.Interaction, total: float, person_to_pay: discord.User, user1: discord.User, user2: discord.User, user3: discord.User = None, user4: discord.User = None, user5: discord.User = None, user6: discord.User = None, user7: discord.User = None, user8: discord.User = None, user9: discord.User = None, user10: discord.User = None) -> None:
    users = [user for user in [user1, user2, user3, user4, user5, user6, user7, user8, user9, user10] if user is not None]
    number_of_people = len(users)
    
    amount_per_person = math.ceil((total / number_of_people) * 100) / 100
    user_mentions = ', '.join(user.mention for user in users)
    embed = discord.Embed(title = 'Bill Splitting', description = f'Each person should pay: ```diff\n+ ${amount_per_person:.2f}\n```', timestamp = datetime.now())
    await interaction.response.send_message(content = f'Hey {user_mentions} pay {person_to_pay.mention} or else 😾', embed = embed)

client.run(DISCORD_TOKEN)



