"""
Reason about a prompt using AI.

This script takes a prompt as input and uses OpenAI's API to generate a reasoned response with o1.
The response is printed to stdout.

Usage:
    ai-kit run reasoning "your prompt here"
"""
from ai_kit.core.llms.openai import OpenAIClient
import asyncio

async def reason(prompt: str) -> str:
    """Execute the reasoning request."""
    client = OpenAIClient()
    res = await client.reason(prompt)
    return res

def main(*args, **kwargs):
    res = asyncio.run(reason(*args, **kwargs))
    print(res)
    
if __name__ == "__main__":
    main()