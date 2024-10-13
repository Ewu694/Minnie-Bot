import discord 

class Task:
    ONE_TIME = 0
    DAILY = 1
    WEEKLY = 2
    MONLTHY = 3
    YEARLY = 4
  
    def __init__(self, task_description: str, task_author: discord.User, repeating_task: int, task_type: str = '0'):
        self.description = task_description
        self.repeating_task = repeating_task
        self.type = task_type
        if task_author:
            self.author = task_author

        def set_type(self, task_type: int) -> None:
            self.type = task_type if task_type in [0, 1, 2, 3, 4] else 0
        def set_description(self, description: str) -> None:
            self.description = description
        def set_repeating_task(self, repeating_task: int) -> None:
            self.repeating_task = repeating_task if repeating_task in [0, 1] else 0
    