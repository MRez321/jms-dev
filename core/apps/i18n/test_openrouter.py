import os
import asyncio
from openai import AsyncOpenAI


async def main():
    client = AsyncOpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
        base_url=os.environ["OPENAI_BASE_URL"],
    )

    response = await client.chat.completions.create(
        model=os.environ["OPENAI_MODEL"],
        messages=[
            {
                "role": "user",
                "content": "Say hello in Persian.",
            }
        ],
    )

    print(response.choices[0].message.content)


asyncio.run(main())