# Minnie-Bot
 Discord Bot named after my girlfriend's moody but cute cat to track whatever tasks you set to it and help organize voting, split bills and other features for groups
 - Voting currently only supports 2 options
  - Can look into other options if suggested by friends or others. If you have suggestions feel free to let me know!
 - Users can make either one-time, daily, weekly, monthly, or yearly tasks for their group that get added to a task-list
 - Users can easily split bills and know who to pay, who needs to be pay, etc.
 - Stores a local task-list hash table within its own client class mapping tasks to a unique ID
# To-Use Bot
Paste this link: N/A (For if I decide to make this bot available to everyone, for now contact me if you wanna use this bot, as long as I know you I'll give you the bot token. For others, please wait until I finish figuring out deploying this bot) 
# Commands (Parameters are all given in order)
1) /hello
 - Description: Says hi to the bot
 - Parameters: None
2) /add_task
 - Description: Adds a task to the task-list
 - Parameters: Description of the Task: str, Repeating Task to determine if this task should be repeated or not (Optional): int, Task Type determines what type of task this will be (Optional): int
  - Repeating Task == 0 it means this task is not to be repeated || Repeating Task == 1 means this task is repeating, by default it is set to repeat infinitely for whatever type of task this can be changed with another function later on /change_repeating_counter 
  - Task Type determines how often this task is repeated:
    - One-time: Default task if type is not set, This type of task cannot be repeated and must be removed with /remove_tasks (will be described later on)
    - Daily: Task will be repeated every 24 hours
    - Weekly: Task will be repeated after a week
    - Monthly: Task will be repeated after 30 days
    - Yearly: Task will repeated after a year (365 days)
    - Keep in mind, by default, all tasks other than the one-time 
3) /show_tasks
 - Description: Displays all the tasks in the task-list in a formatted way
 - Parameters: None
4) /remove_task
 - Description: Removes a task from the task-list using a user given task-id
 - Parameter: Task-ID: int
 - If the task-list is empty or the task couldn't be found within the task-list, message will let user know and provide further instructions
 - If task-ID is found then if its a one-time task or a non-repeating task, it'll be deleted. Else if it is a repeating task, it will reschedule it
5) /clear_tasks
 - Description: Removes all the tasks in the task-list hash table
 - Parameters: None
6) /change_task_type
 - Description: Changes the type of a task
 - Parameters: Task-ID: int, Task type the user of the command wants to change the task into: int
7) /change_task_description
 - Description: Changes the description of a task given its ID
 - Parameters: Task-ID: int, Task description the user of the command wants to change the current tasks description into: str
8) /change_task_counter
 - Description: Changes the amount of times a task will repeat if it is a repeating task
 - Parameters: Task-ID: int, Repeating Counter to be set onto current one: str
  - Repeating Counter string should either be inf or a number, otherwise it'll default to 1
9) /vote
 - Description: Vote for a topic provided by the message/command author given two options for a user decided amount of time
 - Parameter: Topic Option: str, First Option: str, Second Option: str, Voting Duration (In Minutes): int  
10) /split_bill
 - Description: Split bill between however many users are given
 - Parameter: Total: float, Person who paid the bill for the group: discord.User, user1, user2, ... user10 (At least 2 users must be provided to split the bill between, the other 8 are optional): discord.User
 - Currently only supports splitting the bill between 10 users
# Developer/Collaborators/Other people who wanna use it Download Guide
1) Fork my Code and open it on your local IDE
2) Add your .env to your local IDE
3) In this .env add the token I give you and change the DISCORD_SERVER_ID to whatever server you're using it on
4) Necessary Packages:
 - pip install discord.pp or python3 -m pip install -U discord.py 
 - pip install python-dotenv or python3 -m pip install -U python-dotenv
6) Run the code and keep it running if you want to use it

## Note
If you find any bugs or any problems, please contact me and let me know so I can fix it ASAP!
Because the bot has a client class that currently stores the tasks locally within itself through an array, as soon as the bot goes down due to updates or whatever reason that may stop it, the tasks will also disappear.
 - To remedy this, I'll look into using a database to store the tasks for each user. I'll start looking into this when I finish my database class.

 
