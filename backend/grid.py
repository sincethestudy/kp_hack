from prompt import Prompt
from chatgpt import complete, complete_parallel


class Grid():

    def __init__(self, prompt, size_hw, model='gpt-3.5-turbo', temperature=1):
        self.prompt = prompt
        self.h, self.w = size_hw 
        self.model = model
        self.temperature = temperature

    def sample_one(self, inputs):
        if isinstance(inputs, str):
            inputs = [inputs]
        messages = self.prompt.format(*inputs)
        return complete(
            messages=messages,
            model=self.model, 
            temperature=self.temperature,
            n=self.h * self.w,
            stream=True
        )
    
    def sample_many(self, inputs, deterministic=True):
        assert len(inputs) == self.h * self.w, f'Expected {self.h * self.w} inputs, got {len(inputs)}'
        messages = [self.prompt.format(*x) for x in inputs]
        return complete_parallel(
            messages=messages,
            model=self.model, 
            temperature=self.temperature if not deterministic else 0,
            n=1,
            stream=True
        )

    
    def mutate(self, inputs, instructions, deterministic=True):
        if isinstance(inputs, str):
            inputs = [inputs]
        mutated_prompts = self.prompt.mutate(instructions, n=(self.h * self.w)-1)
        messages = [prompt.format(*inputs) for prompt in [self.prompt] + mutated_prompts]
        return complete_parallel(
            messages=messages,
            model=self.model,
            temperature=self.temperature if not deterministic else 0,
            n=1,
            stream=True
        )


def test_sample_one():
    prompt = Prompt(
        system_message = "You're an edgy chatbot",
        user_message = "Explain the lore behind {}"
    )
    inputs = "Tony, the construction worker"

    grid = Grid(prompt, (2, 2))
    for text, idx in grid.sample_one(inputs):
        if idx == 0:
            print(text, end='', flush=True)


def test_sample_many():
    prompt = Prompt(
        system_message = "You're an edgy chatbot",
        user_message = "Make a really long funny joke about {0} and {1}"
    )

    animals = [('frogs', 'cats'),
               ('spiders', 'whales'),
               ('fish', 'snails'),
               ('birds', 'lizards'),]

    grid = Grid(prompt, (2, 2))
    for text, idx in grid.sample_many(animals, deterministic=False):
        if idx == 0:
            print(text, end='', flush=True)


def test_mutate():
    prompt = Prompt(
        system_message='You continue the story.',
        user_message='You are an {0} wizard named {1}.',
    )
    inputs = ['acrobatic', 'Jeleel']
    mutation_instructions = 'Make the story about a different fantasy character'

    grid = Grid(prompt, (2, 2))
    for text, idx in grid.mutate(inputs, mutation_instructions, deterministic=False):
        if idx == 0:
            print(text, end='', flush=True)

if __name__ == '__main__':
    test_sample_one()
    # test_sample_many()
    # test_mutate()