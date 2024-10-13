import discord 

class Task:
    ONE_TIME = 0
    DAILY = 1
    WEEKLY = 2
    YEARLY = 3
  
    def __init__(self, task_description: str, task_author: discord.User, task_type: str = '0'):
        self.description = task_description
        self.type = task_type
        if task_author:
            self.author = task_author

        def set_type(self, task_type: int) -> None:
            self.type = task_type if task_type in [0, 1, 2, 3] else 0
        def set_description(self, description: str) -> None:
            self.description = description
    