import discord 

class Task:
    ONE_TIME = 0
    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3
    YEARLY = 4
    TESTING = 5
  
    def __init__(self, task_description: str, task_author: discord.User, repeating_task: int, task_type: str = '0'):
        self.description = task_description
        self.repeating_task = repeating_task
        if repeating_task == 1:
            self.repeating_counter = 'inf'
        self.type = task_type
        if task_author:
            self.author = task_author

    def set_type(self, task_type: int) -> None:
        self.type = task_type if task_type in [0, 1, 2, 3, 4, 5] else 0

    def set_description(self, description: str) -> None:
        self.description = description

    def set_repeating_task(self, repeating_task: int) -> None:
        self.repeating_task = repeating_task if repeating_task in [0, 1] else 0
        if self.repeating_task == 1:
            self.repeating_counter = 'inf'
        else:
            self.repeating_counter = 0
            
    def set_repeating_counter(self, repeating_counter: str) -> None:
        if self.repeating_task == 'inf':
            self.repeating_counter = repeating_counter
        elif repeating_counter.isdigit():
            self.repeating_counter = int(repeating_counter)
        else:
            self.repeating_counter = 1
            
    def convert_repeating_counter_to_int(self) -> None:
        if isinstance(self.repeating_counter, str) and self.repeating_counter.isdigit():
            self.repeating_counter = int(self.repeating_counter)