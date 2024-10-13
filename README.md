# Minnie-Bot
 Discord Bot named after my girlfriend's moody but cute cat to track whatever tasks you set to it and help organize voting for whatever needed
 - Voting currently only supports 2 options
  - Can look into other options if suggested by friends or others. If you have suggestions feel free to let me know!
 - Task list is very simple and shows every task, doesn't say daily, weekly, etc.
  - Next up may be for me to seperate into daily, weekly, etc.
# To-Use Bot
Paste this link: N/A (For if I decide to make this bot available to everyone, for now contact me if you wanna use this bot, as long as I know you I'll give you the bot token. For others, please wait until I finish figuring out deploying this bot) 


# Developer/Collaborators/Other people who wanna use it Download Guide
1) Fork my Code and open it on your local IDE
2) Add your .env to your local IDE
3) In this .env add the token I give you and change the DISCORD_SERVER_ID to whatever server you're using it on
4) Necessary Packages:
 - pip install discord.pp or python3 -m pip install -U discord.py 
 - pip install python-dotenv or python3 -m pip install -U python-dotenv
6) Run the code and keep it running if you want to use it

## Note
Because the bot has a client class that currently stores the tasks locally within itself through an array, as soon you stop running this code, the tasks will also disappear.
 - To remedy this, I'll look into using a database to store the tasks for each user. I'll start looking into this when I finish my database class. For now the main functionality is the voting system
 
