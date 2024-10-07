from random import choice, randint

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower() 

    if lowered == '':
        return 'Hi? :('
    elif lowered == 'hi' or 'hello':
        return 'Howdy! :3'
    else:
        return randint(1, 100)