from chatgpt import complete_parallel


def generate_parallel(system_message, inputs, prompts):
    messages = [
        [
            {'role': 'system', 'content': system_message},
            {'role': 'user', 'content': prompt.format(*inputs)}
        ]
        for prompt in prompts
    ]
    return complete_parallel(
        messages=messages,
        model='gpt-3.5-turbo',
        temperature=1,
        stream=True
    )