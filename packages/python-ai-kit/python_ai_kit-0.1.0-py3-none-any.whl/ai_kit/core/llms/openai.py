from openai import AsyncOpenAI
from typing import AsyncIterator

class OpenAIClient:
    def __init__(self, model: str = "gpt-4o", reasoning_model: str = "o1-mini"):
        self.client = AsyncOpenAI()
        self.model = model
        self.reasoning_model = reasoning_model

    async def stream(self, prompt: str) -> AsyncIterator[str]:
        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        for chunk in stream:
            yield chunk.choices[0].delta.content

    async def reason(self, prompt: str) -> str:
        res = await self.client.chat.completions.create(
            model=self.reasoning_model,
            messages=[{"role": "user", "content": prompt}],
        )
        return res.choices[0].message.content