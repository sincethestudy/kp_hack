import re
from chatgpt import complete


mutate_system_message = "You modify the user's prompt according to their instructions. \
Do not add or remove the placeholders in the string such as {}, {0}, {name} etc."

mutate_user_message = """\
{0}

Modify the above prompt according to the following instructions. \
DO NOT add or remove the placeholders in the string such as {{}}, {{0}}, {{name}} etc.

"""

def mutate_prompt(prompt, instructions, n=1):
    system_message = mutate_system_message
    user_message = mutate_user_message + instructions

    messages = [
        {'role': 'system', 'content': system_message}, 
        {'role': 'user', 'content': user_message.format(prompt)}
    ]

    placeholders = find_placeholders(prompt)

    mutated_prompts = complete(messages, model='gpt-3.5-turbo', n=n*2, stream=False, temperature=1.5)
    mutated_prompts = [m for m in mutated_prompts if find_placeholders(m) == placeholders][:n]

    return mutated_prompts


def find_placeholders(s):
    return re.findall(r'{[^}]*}', s)
