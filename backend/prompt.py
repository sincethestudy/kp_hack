from chatgpt import complete


mutate_system_message = "You modify the user's prompt according to their instructions. \
Do not add or remove the placeholders in the string such as {}, {0}, {name} etc."

mutate_user_message = """\
{0}

Modify the above prompt according to the following instructions. \
DO NOT add or remove the placeholders in the string such as {{}}, {{0}}, {{name}} etc.

"""

class Prompt():
    MUTATION_TEMPERATURE = 1.5

    def __init__(self, system_message, user_message):
        self.system_message = system_message
        self.user_message = user_message
    
    def format(self, *args):
        try:
            messages = [
                {'role': 'system', 'content': self.system_message}, 
                {'role': 'user', 'content': self.user_message.format(*args)}
            ]
        except (IndexError, KeyError) as e:
            print(f'ERROR: Could not format prompt with args:\n{args}')
            raise e
        
        return messages
    
    def mutate(self, instructions, n=1):
        system_message = mutate_system_message
        user_message = mutate_user_message + instructions
        messages = Prompt(system_message, user_message).format(self.user_message)
        mutated_prompts = complete(messages, model='gpt-4', n=n, stream=False, temperature=self.MUTATION_TEMPERATURE)
        mutated_prompts = [Prompt(self.system_message, p) for p in mutated_prompts]
        return mutated_prompts


def test_mutation():
    prompt = Prompt(
        system_message='You continue the story.',
        user_message='You are an {0} wizard named {1}.',
    )
    for mutated in prompt.mutate('Make the story about a different fantasy character', n=3):
        print(mutated.user_message)


if __name__ == '__main__':
    test_mutation()