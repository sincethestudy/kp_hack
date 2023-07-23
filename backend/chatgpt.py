import asyncio
import aiostream
import openai


from logger import log_messages


def complete(messages, **kwargs):
    stream = kwargs.get('stream', False)

    if stream:
        return complete_streamed(messages, **kwargs)

    response = openai.ChatCompletion.create(
        messages=messages,
        **kwargs
    )

    if kwargs.get('n', 1) == 1:
        result = response.choices[0].message.content
    else:
        result = [choice.message.content for choice in response.choices]

    messages += [{'role': 'assistant', 'content': result}]
    log_messages(messages)
    return result
    

def complete_streamed(messages, **kwargs):
    response = openai.ChatCompletion.create(
        messages=messages,
        **kwargs
    )

    result = ['' for _ in range(kwargs.get('n', 1))]
    for chunk in response:
        for choice in chunk.choices:
            if not choice.delta:
                continue
            text = choice.delta.content
            if not text:
                continue
            idx = choice.index
            result[idx] += text
            yield (text, idx)

    messages += [{'role': 'assistant', 'content': result}]
    log_messages(messages)


def complete_parallel(messages, **kwargs):
    stream = kwargs.get('stream', False)
    n = kwargs.get('n', 1)
    assert n == 1, 'n > 1 not supported for parallel completion'

    if stream:
        return complete_parallel_streamed(messages, **kwargs)

    async def _complete_parallel():
        tasks = [acomplete(messages=m, **kwargs) for m in messages]
        return await asyncio.gather(*tasks)
    
    return asyncio.run(_complete_parallel())


async def acomplete(messages, i=None, **kwargs):
    n = kwargs.get('n', 1)
    stream = kwargs.get('stream', False)
    assert not stream, 'stream=True not supported in acomplete(), use acomplete_streamed() instead'

    response = await openai.ChatCompletion.acreate(
        messages=messages,
        **kwargs,
    )

    if n == 1:
        result = response.choices[0].message.content
    else:
        result = [choice.message.content for choice in response.choices]

    messages += [{'role': 'assistant', 'content': result}]
    log_messages(messages)
    return result


def complete_parallel_streamed(messages, **kwargs):
    async def _complete_parallel_streamed():
        agenerators = [
            acomplete_streamed(messages=m, idx=i, **kwargs)
            for i, m in enumerate(messages)
        ]

        async with aiostream.stream.merge(*agenerators).stream() as streamer:
            async for text, idx in streamer:
                yield text, idx

    agenerator = _complete_parallel_streamed()
    loop = asyncio.get_event_loop()
    return iter_over_async(agenerator, loop)


async def acomplete_streamed(messages, idx, **kwargs):
    response = await openai.ChatCompletion.acreate(messages=messages, **kwargs)
    result = ''
    async for chunk in response:
        choice = chunk.choices[0]
        if not choice.delta:
            continue
        text = choice.delta.content
        if not text:
            continue
        result += text
        yield (text, idx)


    messages += [{'role': 'assistant', 'content': result}]
    log_messages(messages)


def iter_over_async(agen, loop):
    agen = agen.__aiter__()
    async def get_next():
        try:
            obj = await agen.__anext__()
            return False, obj
        except StopAsyncIteration:
            return True, None
    while True:
        done, obj = loop.run_until_complete(get_next())
        if done:
            break
        yield obj